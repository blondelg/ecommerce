from django.views import generic
from apps_custom.importer.forms import UploadTypeSelectForm
from django.http import HttpResponseRedirect
from oscar.apps.dashboard.catalogue.views import ProductListView as CoreProductListView
from oscar.apps.dashboard.catalogue.views import ProductCreateUpdateView as CoreProductCreateUpdateView
from oscar.apps.dashboard.catalogue.views import ProductDeleteView as CoreProductDeleteView
from apps_fork.partner.models import Partner
from django.contrib.auth.models import User
from apps_fork.dashboard.catalogue.tables import ProductTable
from apps_fork.catalogue.models import Product

from apps_fork.dashboard.catalogue.formsets import StockRecordFormSet


from oscar.core.loading import get_model

Tag = get_model('content', 'Tag')
ContentProductTag = get_model('content', 'ContentProductTag')



def get_partner_id(user_id):
    """ get partner id from user_id """
    return Partner.objects.get(users=User.objects.get(id=user_id)).pk

def filter_products(queryset, user):

    if user.is_staff:
        return queryset
    # Select partner attached o the user id
    partner_id = get_partner_id(user.pk)
    return queryset.filter(partner_id=partner_id).distinct()

class ProductListView(CoreProductListView):
    # update product list view table
    table_class = ProductTable
    def filter_queryset(self, queryset):
        return filter_products(queryset, self.request.user)

    def get_table(self, **kwargs):
        if 'recently_edited' in self.request.GET:
            kwargs.update(dict(orderable=False))

        table = super().get_table(**kwargs)
        table.caption = self.get_description(self.form)
        # hide partned column if user is not is_staff
        if not self.request.user.is_staff:
            table.exclude = ('partner')
        return table

class ProductCreateUpdateView(CoreProductCreateUpdateView):

    #stockrecord_formset = StockRecordFormSet

    def get_queryset(self):
        return filter_products(Product.objects.all(), self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['product_class'] = self.product_class
        kwargs['parent'] = self.parent
        # Add Partner that has added the product
        try:
            kwargs['partner'] = Partner.objects.get(users = self.request.user)
        except:
            pass

        return kwargs
        
    def create_tags(self, tags, object):
        """ from a given form, create product tags and return form with empty tag list """
            
        for tag in tags:
            # Check if tag exists, if not, create it
            try:
                t = Tag.objects.get(name=tag)
            except:
                t = Tag(name=tag)
                t.save()
                
            # Check if product tag exits, if not, create it
            try:
                product_tag = ContentProductTag.objects.get(content_object=object, tag=t)
            except:
                ContentProductTag(content_object=object, tag=t).save()
        
        
    def forms_valid(self, form, formsets):
        """
        Save all changes and display a success url.
        When creating the first child product, this method also sets the new
        parent's structure accordingly.
        """
        if self.creating:
            self.handle_adding_child(self.parent)
        else:
            # a just created product was already saved in process_all_forms()
            tags = form.cleaned_data['tags']
            if len(tags) == 0:
                self.object = form.save()
            else:
                form.cleaned_data['tags'] = []
                self.object = form.save()
                self.create_tags(tags,self.object)


        # Save formsets
        for formset in formsets.values():
            formset.save()

        for idx, image in enumerate(self.object.images.all()):
            image.display_order = idx
            image.save()

        return HttpResponseRedirect(self.get_success_url())
        
    def process_all_forms(self, form):
        """
        Short-circuits the regular logic to have one place to have our
        logic to check all forms
        """
        # Need to create the product here because the inline forms need it
        # can't use commit=False because ProductForm does not support it
        if self.creating and form.is_valid():
            tags = form.cleaned_data['tags']
            if len(tags) == 0:
                self.object = form.save()
            else:
                form.cleaned_data['tags'] = []
                self.object = form.save()
                self.create_tags(tags,self.object)

        formsets = {}
        for ctx_name, formset_class in self.formsets.items():
            formsets[ctx_name] = formset_class(self.product_class,
                                               self.request.user,
                                               self.request.POST,
                                               self.request.FILES,
                                               instance=self.object)

        is_valid = form.is_valid() and all([formset.is_valid()
                                            for formset in formsets.values()])

        cross_form_validation_result = self.clean(form, formsets)
        if is_valid and cross_form_validation_result:
            return self.forms_valid(form, formsets)
        else:
            return self.forms_invalid(form, formsets)

    # form_valid and form_invalid are called depending on the validation result
    # of just the product form and redisplay the form respectively return a
    # redirect to the success URL. In both cases we need to check our formsets
    # as well, so both methods do the same. process_all_forms then calls
    # forms_valid or forms_invalid respectively, which do the redisplay or
    # redirect.
    form_valid = form_invalid = process_all_forms
                

class ProductDeleteView(CoreProductDeleteView):
    def get_queryset(self):
        return filter_products(Product.objects.all(), self.request.user)


# new class
class ProductUploadCSVRedirectView(generic.RedirectView):
    permanent = False
    UploadType_form_class = UploadTypeSelectForm

    def get_redirect_url(self):
        if self.request.method == 'POST' and self.request.FILES['myfile']:
            csvFile = self.request.FILES['myfile']
            form = UploadTypeSelectForm(self.request.POST)
            if form.is_valid():
                upload_type = form.cleaned_data['type']

            # check file size
            if csvFile.size > settings.CSV_MAX_SIZE*1024000:

                # return an error message
                return reverse('dashboard:catalogue-product-list')

            fs = FileSystemStorage(location = settings.CSV_ROOT)
            filename = fs.save(csvFile.name, csvFile)
            uploaded_file_url = os.path.join(settings.CSV_ROOT, filename)

            uploader = csv_uploader(uploaded_file_url)
            uploader.upload(upload_type)

            # import csv


            return reverse('dashboard:catalogue-product-list')
        return reverse('dashboard:catalogue-product-list')

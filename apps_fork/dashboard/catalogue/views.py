from django.views import generic
from apps_custom.importer.forms import UploadTypeSelectForm
from oscar.apps.dashboard.catalogue.views import ProductListView as CoreProductListView
from oscar.apps.dashboard.catalogue.views import ProductCreateUpdateView as CoreProductCreateUpdateView
from oscar.apps.dashboard.catalogue.views import ProductDeleteView as CoreProductDeleteView
from oscar.apps.partner.models import Partner
from django.contrib.auth.models import User
from apps_fork.dashboard.catalogue.tables import ProductTable

def filter_products(queryset, user):
    # Select partner attached to the user id
    partner_id = Partner.objects.get(users=User.objects.get(id=user.pk)).pk
    if user.is_staff:
        return queryset
    return queryset.filter(partner_id=partner_id).distinct()

class ProductListView(CoreProductListView):
    # update product list view table
    table_class = ProductTable
    def filter_queryset(self, queryset):
        return filter_products(queryset, self.request.user)

class ProductCreateUpdateView(CoreProductCreateUpdateView):
    def get_queryset(self):
        return filter_products(Product.objects.all(), self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['product_class'] = self.product_class
        kwargs['parent'] = self.parent
        # Add Partner that has added the product
        kwargs['partner'] = Partner.objects.get(users = self.request.user)
        print(self.request.user.pk)

        return kwargs

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

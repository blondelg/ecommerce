from django.views import generic
from apps_custom.importer.forms import UploadTypeSelectForm


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

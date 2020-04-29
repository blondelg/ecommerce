#-*- coding: utf-8 -*-
from oscar.apps.dashboard.catalogue.views import ProductListView as CoreProductListView
from forms import CsvForm

print("DEBUG VIEWS")

class ProductListView(CoreProductListView):
    template_name = 'oscar/dashboard/catalogue/p_list.html'
    def simple_upload(self):
        if self.request.method == 'POST' and self.request.FILES['myfile']:
            myfile = self.request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            return render(self.request, 'core/simple_upload.html', {
                'uploaded_file_url': uploaded_file_url
            })
        return render(self.request, 'core/simple_upload.html')

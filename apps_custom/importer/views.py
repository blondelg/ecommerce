from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage

def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        print('DEBUG')
        myfile = request.FILES['myfile']
        fs = FileSystemStorage(base_url='csv/')
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'core/simple_upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    next = request.POST.get('next', '/')
    return HttpResponseRedirect(next)

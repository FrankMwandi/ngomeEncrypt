from django.shortcuts import render
from django.http import HttpResponse
from .forms import UploadFileForm
from .utils import encrypt_file
from .models import EncryptionLog

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            password = form.cleaned_data['password']
            encrypted_data = encrypt_file(file, password)
            
            # Log the usage
            EncryptionLog.objects.create(
                ip_address=request.META.get('REMOTE_ADDR'),
                filename=file.name
            )

            response = HttpResponse(encrypted_data['ciphertext'], content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{file.name}.enc"'
            return response
    else:
        form = UploadFileForm()
    return render(request, 'Core_app/upload.html', {'form': form})


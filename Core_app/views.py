from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UploadFileForm
from .utils import encrypt_file, decrypt_file
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
                filename=file.name,
                action='encrypt'
            )

            response = HttpResponse(encrypted_data.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{file.name}.enc"'
            return response
    else:
        form = UploadFileForm()
    return render(request, 'Core_app/upload.html', {'form': form})

def decrypt_file_view(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            encrypted_file = request.FILES['file']
            password = form.cleaned_data['password']
            try:
                decrypted_content = decrypt_file(encrypted_file, password)

                # Log the usage
                EncryptionLog.objects.create(
                    ip_address=request.META.get('REMOTE_ADDR'),
                    filename=encrypted_file.name,
                    action='decrypt'
                )

                response = HttpResponse(decrypted_content, content_type='application/octet-stream')
                response['Content-Disposition'] = f'attachment; filename="{encrypted_file.name[:-4]}"'
                return response
            except Exception as e:
                form.add_error(None, 'Decryption failed. Invalid password or corrupted file.')
    else:
        form = UploadFileForm()
    return render(request, 'Core_app/decrypt.html', {'form': form})

from django.shortcuts import render, redirect
from .forms import DocumentForm,CustomLoginForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from xhtml2pdf import pisa
from io import BytesIO
from django.template.loader import render_to_string
from django.http import HttpResponse
import os
import pdfkit
import boto3
from django.conf import settings
from .decorators import department_required

def home(request):
    return HttpResponse("Hello, this is the home page.")


def upload_document(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)  
            document.save()  
            
            # Define S3 client
            s3_client = boto3.client(
                's3',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_S3_REGION_NAME,
            )

            # File information
            file = request.FILES['file']
            s3_key = f"invoice/{document.id}/{file.name}"

            # Upload to S3
            s3_client.upload_fileobj(
                file.file,
                settings.AWS_STORAGE_BUCKET_NAME,
                s3_key,
                ExtraArgs={'ContentType': file.content_type}
            )

            # Update file field in model to reflect S3 path
            document.file.name = s3_key
            document.save()

            return redirect('upload_success')
    else:
        form = DocumentForm()

    return render(request, 'upload.html', {'form': form})



def upload_success(request):
    return HttpResponse("File uploaded successfully to S3!")


def generate_pdf(request):
    html_content = render_to_string('Treasury-byte-bill.html', {})
    landscape_css = """
    <style>
        @page {
            size: A1 landscape;
            margin: 1cm;
        }
        
    </style>
    """
    html_content = landscape_css + html_content

    pdf_file = BytesIO()
    pisa_status = pisa.CreatePDF(html_content, dest=pdf_file)
    
    if pisa_status.err:
        return HttpResponse("Error generating PDF", status=500)
    pdf_file.seek(0)
    return HttpResponse(
        pdf_file.read(),
        content_type='application/pdf',
        headers={'Content-Disposition': 'attachment; filename="generated_document.pdf"'}
        
    )

def login_view(request):
    form = CustomLoginForm(request, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect to home or a dashboard
    return render(request, 'login.html', {'form': form})

@login_required
@department_required('data')
def data_department_view(request):
    return render(request, 'data_department.html')

@login_required
@department_required('infra')
def infra_department_view(request):
    return render(request, 'infra_department.html')

@login_required
@department_required('digital_marketing')
def digital_marketing_department_view(request):
    return render(request, 'digital_marketing_department.html')



def logout_view(request):
    logout(request)
    return redirect('login')
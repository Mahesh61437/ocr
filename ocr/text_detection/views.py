import os
import io
from google.cloud import vision

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

from .forms import UploadForm, DownloadForm


def detect_document(image_file=None, url=None):
    """Detects document features in an image."""
    client = vision.ImageAnnotatorClient()

    if url is not None:
        image = vision.Image()
        image.source.image_uri = url
    else:
        image = vision.Image(content=image_file)

    response = client.document_text_detection(image=image)

    word_text = ''

    for page in response.full_text_annotation.pages:
        for block in page.blocks:

            for paragraph in block.paragraphs:

                for word in paragraph.words:
                    word_text += ''.join([
                        symbol.text for symbol in word.symbols
                    ])

                    word_text += ' '

    if response.error.message:
        raise Exception()

    return word_text


# Create your views here.
def process_image(request):

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        image_data = None
        image_url = None
        form = UploadForm(request.POST or None, request.FILES or None)
        # check whether it's valid:
        if form.is_valid():

            if request.FILES.get('image'):
                uploaded_image = request.FILES['image']
                image_data = uploaded_image.file.read()
            elif request.POST.get('url'):
                image_url = request.POST['url']
            else:
                return render(request, 'upload.html', {'form': form,
                                                       "errors": "invalid input. Expecting a image or a url"})

            output = detect_document(image_file=image_data, url=image_url)
            request.session['recognized_data'] = output

            return redirect('/result')
    # if a GET (or any other method) we'll create a blank form
    else:
        form = UploadForm()

    return render(request, 'upload.html', {'form': form})


def home(request):
    return render(request, 'home.html')


def result(request):

    form = DownloadForm(initial={"output": request.session['recognized_data']})
    return render(request, 'download.html', {'form': form})


def download_result(request):
    file_data = request.session['recognized_data']

    response = HttpResponse(file_data, content_type='application/text charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="output.txt"'
    return response

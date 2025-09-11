from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def home_page(request):
    return render(request, 'posts/home.html')

def post_form(request):
    return render(request, 'posts/postForm.html')
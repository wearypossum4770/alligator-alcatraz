from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader


def main(request):
    return render(request, "index.html")

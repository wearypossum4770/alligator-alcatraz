from django.shortcuts import render


def list_all_posts(request):
    context = {}
    return render(request, "", context=context)

from django.shortcuts import render

def serviceworker(request):
    context = {}
    template = "pwa/serviceworker.js"
    return render(request, template, context, content_type="application/javascript")

def manifest(request):
    context = {}
    template = "pwa/manifest.json"
    return render(request, template, context, content_type="application/json")

def offline(request):
    context = {}
    template = "pwa/offline.html"
    return render(request, template, context)

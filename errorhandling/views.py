from django.shortcuts import render
from django.views.generic.base import View
from django.template import loader
from django.http.response import HttpResponse


# Create your views here.
class PurchaseErrorView(View):
    def get(self, request):
        template = loader.get_template("errorhandling/purchaseErrorPage.html")
        context = {}

        return HttpResponse(template.render(context, request))


class StoreErrorView(View):
    def get(self, request):
        template = loader.get_template("errorhandling/storeErrorPage.html")
        context = {}

        return HttpResponse(template.render(context, request))
    

class Error404View(View):
    def get(self, request):
        template = loader.get_template("errorhandling/404page.html")
        context = {}

        return HttpResponse(template.render(context, request))

class Error500View(View):
    def get(self, request):
        template = loader.get_template("errorhandling/500page.html")
        context = {}

        return HttpResponse(template.render(context, request))
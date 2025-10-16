# главная страница и простые представления

from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.shortcuts import render

from django.views.generic import TemplateView




@method_decorator(ensure_csrf_cookie, name='dispatch')
class HomeView(View):
    def get(self, request):
        return render(request, 'app/home.html')









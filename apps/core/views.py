from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View


class HomeView(View):
    template_name = "home.html"

    def get(self, request):
        ctx = {}
        return render(request, self.template_name, ctx)

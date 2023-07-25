from django.urls import path, include, re_path
from django.views.generic import TemplateView

urlpatterns = [
    path("", include("rest_framework.urls")),
    path("", include("accounts.urls")),
]

urlpatterns += [re_path(r"^.*", TemplateView.as_view(template_name="index.html"))]

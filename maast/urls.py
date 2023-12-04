from django.urls import path

from .views import home_page_view, organizations_view

urlpatterns = [
    path("", home_page_view, name="home"),
    path("organizations/", organizations_view, name="organizations"),
]

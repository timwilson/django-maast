from django.urls import path

from maast.views.organizations import home_page_view, organizations_view

urlpatterns = [
    path("", home_page_view, name="home"),
    path("organizations/", organizations_view, name="organizations"),
]

from django.http import HttpResponse
from django.shortcuts import render

from maast.services.http_client import MaastHTTPClient


def home_page_view(request):
    return HttpResponse("Hello, World!")


def fetch_organizations():
    url = "http://maast-api:8000/v1/organizations"
    with MaastHTTPClient() as client:
        response = client.get(url)
    return response.json()


def organizations_view(request):
    organizations = fetch_organizations()
    return render(request, "organizations.html", {"organizations": organizations})

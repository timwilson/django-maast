from django.http import HttpResponse
from django.shortcuts import render

# from maast.models import Organization
from maast.services.http_client import MaastHTTPClient


def home_page_view(request):
    return HttpResponse("Hello, World!")


def fetch_organizations():
    url = "http://maast-api:8000/v1/organizations"
    with MaastHTTPClient() as client:
        response = client.get(url)
    organization_data = response.json()

    return organization_data


def organizations_view(request):
    organizations = fetch_organizations()

    return render(request, "organizations.html", {"organizations": organizations})

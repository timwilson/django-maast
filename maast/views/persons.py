from typing import Dict

from django.http import HttpRequest, JsonResponse

from maast.services.http_client import MaastHTTPClient


def fetch_person_record(slug: str) -> Dict:
    url = f"http://maast-api:8000/v1/persons/{slug}/records"
    with MaastHTTPClient() as client:
        response = client.get(url)
    return response.json()


def person_profile_view(request: HttpRequest, slug: str) -> JsonResponse:
    person_record = fetch_person_record(slug)
    return JsonResponse(person_record)

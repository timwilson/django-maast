from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from typing import List, Dict, Any

from maast.models import Score
from maast.services.group_and_sort import validate_and_sort_records
from maast.services.http_client import MaastHTTPClient


def fetch_person_scores(
    round_id: int, age_division: str, gender: str, equipment_class: str
) -> List[Dict[str, Any]]:
    url = f"{settings.API_HOST}/v1/rounds/{round_id}/scores"
    params = {
        "age_division": age_division,
        "gender": gender,
        "equipment_class": equipment_class,
    }

    with MaastHTTPClient() as client:
        response = client.get(url, params=params)
    return response.json()


def get_valid_scores_by_round_and_division(
    request: HttpRequest, round_id: int
) -> HttpResponse:
    age_division = request.GET.get("age_division")
    gender = request.GET.get("gender")
    equipment_class = request.GET.get("equipment_class")

    raw_scores = fetch_person_scores(round_id, age_division, gender, equipment_class)
    sort_keys = ["rank"]
    processed_sorted_scores = validate_and_sort_records(raw_scores, Score, sort_keys)

    # Assuming round_name is available from the first record or another source
    round_name = raw_scores[0]["round"]["name"] if raw_scores else ""
    division = f"{age_division} {gender} {equipment_class}"
    context = {
        "round_name": round_name,
        "division": division,
        "scores": processed_sorted_scores,
    }

    return render(request, "scores_by_round_and_division.html", context)

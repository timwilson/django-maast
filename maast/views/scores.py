from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from typing import List, Dict, Any

from maast.models import Score
from maast.services.group_and_sort import validate_and_sort_records
from maast.services.http_client import MaastHTTPClient


def fetch_round_scores_by_division(
    round_id: int, age_division: str, gender: str, equipment_class: str
) -> List[Dict[str, Any]]:
    """

    Fetch Round Scores By Division

    This method is used to fetch round scores based on the specified division.

    Parameters:
    - `round_id` (int): The ID of the round for which scores should be fetched.
    - `age_division` (str): The age division for which scores should be fetched.
    - `gender` (str): The gender for which scores should be fetched.
    - `equipment_class` (str): The equipment class for which scores should be fetched.

    Returns:
    - `List[Dict[str, Any]]`: A list of dictionaries containing the round scores. Each
    dictionary represents a score and contains various key-value pairs.

    """
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
    """

    This method, `get_valid_scores_by_round_and_division`, retrieves valid scores for a specific round and
    division from the server's database and renders them in a web page using Django's `render` function.

    Parameters:
    - `request` (`HttpRequest`): A Django `HttpRequest` object representing the client's HTTP request.
    - `round_id` (`int`): An integer representing the ID of the round for which to retrieve scores.

    Returns:
    - `HttpResponse`: A Django `HttpResponse` object representing the rendered scores page.

    Example Usage:
    ```python
    # Assumptions:
    # - Proper Django imports are already done
    # - The required functions and modules are imported or available

    def my_view(request):
        round_id = 1  # Example round ID
        response = get_valid_scores_by_round_and_division(request, round_id)
        return response
    ```
    """
    age_division = request.GET.get("age_division")
    gender = request.GET.get("gender")
    equipment_class = request.GET.get("equipment_class")

    raw_scores = fetch_round_scores_by_division(
        round_id, age_division, gender, equipment_class
    )
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

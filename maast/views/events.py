from typing import List, Dict, Any

from django.conf import settings
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

from maast.models import Score
from maast.services.group_and_sort import validate_and_sort_records
from maast.services.http_client import MaastHTTPClient


def fetch_event_scores(event_id: int) -> List[Dict[str, Any]]:
    """
    Fetches the scores for a given event.

    Args:
        event_id (int): The ID of the event.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing the scores of the event.

    Example:
        >>> fetch_event_scores(123)
        [{'score': 9.5, 'player': 'John'}, {'score': 8.7, 'player': 'Alice'}, ...]
    """
    url = f"{settings.API_HOST}/v1/events/{event_id}/scores"
    with MaastHTTPClient() as client:
        response = client.get(url)
    return response.json()


def get_valid_scores_by_event(request: HttpRequest, event_id: int) -> HttpResponse:
    """
    Get valid scores by event.

    This method retrieves raw scores for a given event, validates and sorts them based on certain criteria,
    and then returns the processed and sorted scores along with event information.

    Parameters:
    - request (HttpRequest): The HTTP request object.
    - event_id (int): The ID of the event for which scores are requested.

    Returns:
    - HttpResponse: The HTTP response object containing the rendered scores by event page.

    """
    raw_scores = fetch_event_scores(event_id)
    sort_keys = [
        "division",
        "-score",
        "-x_count",
    ]
    processed_sorted_scores = validate_and_sort_records(raw_scores, Score, sort_keys)

    event_name = raw_scores[0]["event"]["name"] if raw_scores else ""
    event_date = raw_scores[0]["event"]["event_date"] if raw_scores else ""
    event_location = (
        raw_scores[0]["event"]["location"]["name_and_location"] if raw_scores else ""
    )
    context = {
        "event_name": event_name,
        "event_date": event_date,
        "event_location": event_location,
        "scores": processed_sorted_scores,
    }

    return render(request, "scores_by_event.html", context)

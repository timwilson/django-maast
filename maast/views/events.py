from collections import defaultdict
from typing import List, Dict, Any

from django.conf import settings
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from meta.views import Meta

from maast.models import Score, Event
from maast.services.group_and_sort import validate_and_sort_records
from maast.services.http_client import MaastHTTPClient


def fetch_event_scores(event_id: int) -> List[Dict[str, Any]]:
    """
    Fetches the scores for a given event.

    Args:
        event_id (int): The ID of the event.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries containing the scores of the event.
    """
    url = f"{settings.API_HOST}/v1/events/{event_id}/scores"
    with MaastHTTPClient() as client:
        response = client.get(url)
    return response.json()


def fetch_events() -> List[Dict[str, Any]]:
    """
    Fetches a list of events from the API.
    """
    url = f"{settings.API_HOST}/v1/events"
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
        "round",
        "-score",
        "-x_count",
    ]
    processed_sorted_scores = validate_and_sort_records(raw_scores, Score, sort_keys)

    event_name = raw_scores[0]["event"]["name"] if raw_scores else ""
    event_date = raw_scores[0]["event"]["event_date"] if raw_scores else ""
    event_location = (
        raw_scores[0]["event"]["location"]["name_and_location"] if raw_scores else ""
    )

    meta = Meta(
        title=f"{event_name} scores",
        site_name="MAA Score Tabulator",
        description=f"Archery scores for MAA members from the {event_name} on {event_date} at {event_location}.",
        url=f"/event/{event_id}/",
        image_object={
            "url": f"{settings.SITE_DOMAIN}/static/img/MAAST-og.png",
            "type": "image/png",
            "width": 1200,
            "height": 628,
            "alt": "MAAST: State record and score database",
        },
        keywords=[event_name],
    )

    context = {
        "event_name": event_name,
        "event_date": event_date,
        "event_location": event_location,
        "scores": processed_sorted_scores,
        "meta": meta,
    }

    return render(request, "scores_by_event.html", context)


def get_valid_events(request: HttpRequest) -> HttpResponse:
    raw_scores = fetch_events()
    sort_keys = ["-start_date"]
    processed_sorted_events = validate_and_sort_records(raw_scores, Event, sort_keys)
    num_events = len(processed_sorted_events)

    # Group events by year
    events_by_year = defaultdict(list)
    for event in processed_sorted_events:
        year = event["start_date"].year
        if event["has_scores"]:
            events_by_year[year].append(event)

    meta = Meta(
        title="MAA Events",
        site_name="MAA Score Tabulator",
        description="List of events for the Minnesota Archers Alliance (MAA) since 2003.",
        url="/events",
        image_object={
            "url": f"{settings.SITE_DOMAIN}/static/img/MAAST-og.png",
            "type": "image/png",
            "width": 1200,
            "height": 628,
            "alt": "MAAST: State record and score database",
        },
        keywords=["events"],
    )

    context = {
        "events_by_year": dict(events_by_year),
        "num_events": num_events,
        "meta": meta,
    }

    return render(request, "event_list.html", context)

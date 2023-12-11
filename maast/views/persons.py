from collections import defaultdict
from typing import Dict, List, Any

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from maast.models import Finish, Record, Score
from maast.services.group_and_sort import validate_and_sort_records
from maast.services.http_client import MaastHTTPClient


def fetch_person_record(person_slug: str) -> Dict:
    """
    Fetches the record of a person from the MAAST API.

    :param person_slug: The slug of the person.
    :type person_slug: str
    :return: The record of the person.
    :rtype: dict
    """
    url = f"{settings.API_HOST}/v1/persons/{person_slug}"
    with MaastHTTPClient() as client:
        response = client.get(url)
    return response.json()


def fetch_person_state_records(person_id: int) -> List[Dict[str, Any]]:
    """
    Fetches the state records of a person with the given person_id from the MAAST API.

    Args:
        person_id (int): The ID of the person to fetch the state records for.

    Returns:
        Dict: A dictionary containing the state records of the person.

    Raises:
        None

    Example:
        >>> fetch_person_state_records(12345)
        {'record_id': 1, 'state': 'California', 'date': '2021-01-01'}
    """
    url = f"{settings.API_HOST}/v1/persons/{person_id}/records"
    with MaastHTTPClient() as client:
        response = client.get(url)
    return response.json()


def fetch_person_scores(person_id: int) -> List[Dict[str, Any]]:
    """
    Fetches the scores of a person with the given person_id from the MAAST API.

    Parameters:
        person_id (int): The ID of the person.

    Returns:
        dict: A dictionary containing the scores of the person.

    """
    url = f"{settings.API_HOST}/v1/persons/{person_id}/scores"
    with MaastHTTPClient() as client:
        response = client.get(url)
    return response.json()


def fetch_person_podiums(person_id: int) -> List[Dict[str, Any]]:
    """
    Fetches the podium finishes of a person with the given person_id from the MAAST API.

    Args:
        person_id (int): The ID of the person to fetch podium finishes for.

    Returns:
        dict: A dictionary containing the podium finishes information for the person.

    Raises:
        None

    Example:
        >>> podiums = fetch_person_podiums(123)
    """
    url = f"{settings.API_HOST}/v1/persons/{person_id}/finishes"
    with MaastHTTPClient() as client:
        response = client.get(url)
    return response.json()


def group_podium_finishes(finishes: List[Dict]) -> Dict[int, int]:
    podium_finishes = defaultdict(int)
    for finish in finishes:
        if finish["place"] in [1, 2, 3]:
            podium_finishes[finish["place"]] += 1
    return dict(podium_finishes)


def get_valid_data_by_person(request: HttpRequest, person_slug: str) -> HttpResponse:
    person_record = fetch_person_record(person_slug)
    person_id = person_record["id"]

    # Retrieve and process state records, if any, from the API
    raw_records = fetch_person_state_records(person_id)
    sort_keys = ["round", "event_name"]
    processed_sorted_records = validate_and_sort_records(raw_records, Record, sort_keys)

    # Retrieve and process scores from the API
    raw_scores = fetch_person_scores(person_id)
    sort_keys = ["round", "event_name"]
    processed_sorted_scores = validate_and_sort_records(raw_scores, Score, sort_keys)

    # Retrieve and process podiums finishes, if any, from the API
    raw_podiums = fetch_person_podiums(person_id)
    sort_keys = ["event_name"]
    processed_sorted_podiums = validate_and_sort_records(raw_podiums, Finish, sort_keys)
    podium_finishes = group_podium_finishes(processed_sorted_podiums)

    person_name = person_record["full_name"]
    context = {
        "person_name": person_name,
        "state_records": processed_sorted_records,
        "scores": processed_sorted_scores,
        "podiums": processed_sorted_podiums,
        "podium_totals": podium_finishes,
    }
    return render(request, "person_profile.html", context)

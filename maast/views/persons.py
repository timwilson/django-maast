from collections import defaultdict
from typing import Dict, List, Any

from django.conf import settings
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render

from maast.models import Finish, Record, Score, Person
from maast.services.group_and_sort import validate_and_sort_records
from maast.services.http_client import MaastHTTPClient


def fetch_person_record(person_slug: str) -> Person:
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
    person = Person(**response.json())
    return person


def fetch_search_results(name: str) -> List[Dict[str, Any]]:
    url = f"{settings.API_HOST}/v1/persons"
    params = {"name": name}

    with MaastHTTPClient() as client:
        response = client.get(url, params=params)
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


def get_podium_finishes_summary(finishes: List[Dict]) -> List[str]:
    podium_finishes = defaultdict(int)
    for finish in finishes:
        if finish["place"] in [1, 2, 3]:
            podium_finishes[finish["place"]] += 1

    # Mapping places to their corresponding emojis
    place_to_emoji = {1: "🥇", 2: "🥈", 3: "🥉"}

    podium_summary = []
    for place, count in podium_finishes.items():
        emoji = place_to_emoji.get(place, "")
        podium_summary.append(f"{count} {emoji}")

    return podium_summary


def get_valid_person_state_records(
    request: HttpRequest, person_id: int
) -> JsonResponse | HttpResponseBadRequest:
    """
    Retrieves valid person state records sorted by round and event name.

    :param request: The HTTP request object.
    :type request: HttpRequest
    :param person_id: The ID of the person.
    :type person_id: int
    :return: The JSON response object containing the processed and sorted records.
             If the request is not an XMLHttpRequest or if DEBUG mode is disabled,
             returns an HttpResponseBadRequest object.
    :rtype: JsonResponse | HttpResponseBadRequest
    """
    if (
        request.headers.get("X-Requested-With") != "XMLHttpRequest"
    ) and not settings.DEBUG:
        return HttpResponseBadRequest()

    raw_records = fetch_person_state_records(person_id)
    sort_keys = ["round", "event_name"]
    processed_sorted_records = validate_and_sort_records(raw_records, Record, sort_keys)
    return JsonResponse(processed_sorted_records, safe=False)


def get_valid_person_scores(
    request: HttpRequest, person_id: int
) -> JsonResponse | HttpResponseBadRequest:
    """

    This method (get_valid_person_scores) fetches the scores of a person with the specified person_id and
    returns them in a JSON response.

    Parameters:
    - request: The HTTP request object.
    - person_id: The ID of the person for whom the scores need to be fetched.

    Returns:
    - If the request headers do not contain "X-Requested-With" as "XMLHttpRequest" and the Django settings.DEBUG is
    False, then this method returns an HttpResponseBadRequest. Otherwise, it fetches the person scores using the
    fetch_person_scores method and performs validation and sorting on them. The sorting is done on the "round"
    and "event_name" keys. The processed and sorted scores are then returned in a JSON response using the
    JsonResponse object.

    Note:
    - This method is suitable for use in Django views or API endpoints.
    - The JsonResponse object is used to wrap the processed scores in a JSON response.

    """
    if (
        request.headers.get("X-Requested-With") != "XMLHttpRequest"
    ) and not settings.DEBUG:
        return HttpResponseBadRequest()

    raw_scores = fetch_person_scores(person_id)
    sort_keys = ["round", "event_name"]
    processed_sorted_scores = validate_and_sort_records(raw_scores, Score, sort_keys)
    return JsonResponse(processed_sorted_scores, safe=False)


def get_valid_person_podiums(
    request: HttpRequest, person_id: int
) -> JsonResponse | HttpResponseBadRequest:
    """
    Get the valid podiums for a person.

    Args:
        request (HttpRequest): The HTTP request object.
        person_id (int): The ID of the person.

    Returns:
        JsonResponse or HttpResponseBadRequest: The JSON response containing the sorted and validated podium
        records if the request is valid and the person's podiums can be fetched. Otherwise, an HTTP response
        with status code 400 (Bad Request) is returned.

    Raises:
        None.

    Example Usage:
        request = HttpRequest()
        person_id = 1
        result = get_valid_person_podiums(request, person_id)
    """
    if (
        request.headers.get("X-Requested-With") != "XMLHttpRequest"
    ) and not settings.DEBUG:
        return HttpResponseBadRequest()

    raw_podiums = fetch_person_podiums(person_id)
    sort_keys = ["age_division", "start_date"]
    processed_sorted_podiums = validate_and_sort_records(raw_podiums, Finish, sort_keys)
    return JsonResponse(processed_sorted_podiums, safe=False)


def search_persons_by_name(
    request: HttpRequest,
) -> JsonResponse | HttpResponseBadRequest:
    if (
        request.headers.get("X-Requested-With") != "XMLHttpRequest"
    ) and not settings.DEBUG:
        return HttpResponseBadRequest()

    name = request.GET.get("name")
    results = fetch_search_results(name)
    return JsonResponse(results, safe=False)


def get_valid_data_by_person(request: HttpRequest, person_slug: str) -> HttpResponse:
    """
    Fetches the valid data for a person and renders their profile page.

    Args:
        request (HttpRequest): The HTTP request object.
        person_slug (str): The slug of the person.

    Returns:
        HttpResponse: The rendered profile page of the person.

    Raises:
        None.

    Example:
        >>> request = HttpRequest()
        >>> person_slug = "john-doe"
        >>> response = get_valid_data_by_person(request, person_slug)
    """
    person = fetch_person_record(person_slug)
    podiums = fetch_person_podiums(person.id)
    podium_summary = get_podium_finishes_summary(podiums)

    context = {"person": person, "podium_summary": podium_summary}
    return render(request, "person_profile.html", context)

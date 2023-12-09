from typing import List, Dict, Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from maast.models import Record
from maast.services.http_client import MaastHTTPClient


def fetch_records_by_round(round_id: int) -> List[Dict[str, Any]]:
    """
    Fetch records by round ID while automatically inserting the necessary X-API-KEY
    to access the API. There's nothing on this site that required read-write access, so a
    read-only key is sufficient.

    Parameters:
    - round_id (int): ID of the round.

    Returns:
    - List[Dict[str, Any]]: A list of records as dictionaries.

    Example Usage:
    >>> fetch_records_by_round(123)
    [{'id': 1, 'name': 'John Doe'}, {'id': 2, 'name': 'Jane Smith'}]
    """
    url = f"http://maast-api:8000/v1/rounds/{round_id}/records"
    with MaastHTTPClient() as client:
        response = client.get(url)
    return response.json()


def records_by_round_view(request: HttpRequest, round_id: int) -> HttpResponse:
    """
    View for fetching and displaying state records by round.

    Parameters:
    - request (HttpRequest): The HTTP request object.
    - round_id (int): The ID of the round for which records are to be fetched.

    Returns:
    - HttpResponse: The HTTP response with the rendered template.
    """
    raw_records = fetch_records_by_round(round_id)

    # Validate and process records using Pydantic
    processed_records = [
        Record(**raw_record).custom_representation() for raw_record in raw_records
    ]

    # Sort the records
    sort_keys = ["age_division", "equipment_class", "gender", "event_name"]
    processed_records.sort(key=lambda x: tuple(x[key] for key in sort_keys))

    # Assuming round_name is available from the first record or another source
    round_name = raw_records[0]["round"]["name"] if raw_records else ""

    context = {"state_records": processed_records, "round_name": round_name}

    return render(request, "records_by_round.html", context)

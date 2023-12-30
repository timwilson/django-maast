from typing import List, Dict, Any

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from meta.views import Meta

from maast.models import Record
from maast.services.group_and_sort import validate_and_sort_records
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
    url = f"{settings.API_HOST}/v1/rounds/{round_id}/records"
    with MaastHTTPClient() as client:
        response = client.get(url)
    return response.json()


def get_valid_records_by_round(request: HttpRequest, round_id: int) -> HttpResponse:
    """
    View for fetching, validating, sorting, and displaying state records by round.
    Parameters:
    - request (HttpRequest): The HTTP request object.
    - round_id (int): The ID of the round for which records are to be fetched, validated, and sorted.
    Returns:
    - HttpResponse: The HTTP response with the rendered template.
    """
    raw_records = fetch_records_by_round(round_id)
    sort_keys = ["age_division", "equipment_class", "gender", "event_name"]
    processed_sorted_records = validate_and_sort_records(raw_records, Record, sort_keys)

    # Assuming round_name is available from the first record or another source
    round_name = raw_records[0]["round"]["name"] if raw_records else ""

    meta = Meta(
        title=f"MAA {round_name} state records",
        site_name="MAA Score Tabulator",
        description=f"MAA state records for the {round_name} round since 2003.",
        url=f"/records/{round_id}",
        image_object={
            "url": f"{settings.SITE_DOMAIN}/static/img/MAAST-og.png",
            "type": "image/png",
            "width": 1200,
            "height": 628,
            "alt": "MAAST: State record and score database",
        },
        keywords=[round_name],
    )

    context = {
        "state_records": processed_sorted_records,
        "round_name": round_name,
        "meta": meta,
    }
    return render(request, "records_by_round.html", context)

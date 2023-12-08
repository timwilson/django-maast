import json
from typing import List, Dict, Any
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render

from maast.models import Record
from maast.services.group_and_sort import sort_data
from maast.services.http_client import MaastHTTPClient


def fetch_records_by_round(round_id: int) -> List[Dict[str, Any]]:
    url = f"http://maast-api:8000/v1/rounds/{round_id}/records"
    with MaastHTTPClient() as client:
        response = client.get(url)
    return response.json()


def records_by_round_view(request: HttpRequest, round_id: int) -> JsonResponse:
    """
    View for fetching and displaying state records by round.

    Parameters:
    - request (HttpRequest): The HTTP request object.
    - round_id (int): The ID of the round for which records are to be fetched.

    Returns:
    - JsonResponse: The JSON response containing the processed records.

    """
    raw_records = fetch_records_by_round(round_id)
    processed_records = []
    round_name = raw_records[0]["round"]["name"]
    for raw_record in raw_records:
        record = Record(
            age_division=raw_record["age_division"]["name"],
            gender=raw_record["gender"]["name"],
            equipment_class=raw_record["equipment_class"]["name"],
            full_name=raw_record["person"]["full_name"],
            person_slug=raw_record["person"]["slug"],
            score=raw_record["pretty_score"],
            event_id=raw_record["event"]["id"],
            event_date=raw_record["event"]["event_date"],
            event_name=raw_record["event"]["name"],
            event_location=raw_record["event"]["location"]["name_and_location"],
        )

        # Convert Record instance to dict and parse date
        record_dict = record.model_dump()
        processed_records.append(record_dict)

    # Convert processed records to JSON
    sorted_processed_records = sort_data(
        processed_records,
        sort_keys=["age_division", "equipment_class", "gender", "event_name"],
    )
    processed_records_json = json.dumps(sorted_processed_records)
    context = {"state_records": processed_records_json, "round_name": round_name}

    return render(request, "records_by_round.html", context)

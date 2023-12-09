from typing import List, Dict, Any


def validate_and_sort_records(
    raw_records: List[Dict[str, Any]], Model: Any, sort_keys: List[str]
) -> List[Dict[str, Any]]:
    """
    Function to validate and sort raw records.
    Parameters:
    - raw_records (Dict[str, Any]): The raw records.
    - Model (Any): The Pydantic model for validation.
    - sort_keys (List[str]): The keys to sort the processed records.
    Returns:
    - list(Dict[str, Any]): The processed sorted records.
    """
    # Validate and Process records using Pydantic
    processed_records = [
        Model(**raw_record).template_representation() for raw_record in raw_records
    ]
    # Sort the records
    processed_records.sort(key=lambda x: tuple(x[key] for key in sort_keys))
    return processed_records

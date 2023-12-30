from datetime import datetime
from typing import List, Dict, Any

from datetime import date, datetime


def none_safe_key(value, reverse=False):
    """
    Create a tuple for sorting purposes that safely handles None values and reverses
    sorting order for integer and date types.

    Parameters:
    - value (Any): The value to be sorted. Can be of any type.
    - reverse (bool, optional): Indicates if the sorting should be in reverse order.
                                Defaults to False.

    Returns:
    - tuple: A tuple where the first element is a boolean indicating the presence of
             non-None values and the second element is the value itself, adjusted for
             reverse sorting if applicable.
    """
    if value is None:
        return (False, value)

    if reverse:
        if isinstance(value, int):
            return (True, -value)
        elif isinstance(value, (date, datetime)):
            # Inverting a date for sorting purposes by converting it to a timestamp
            max_date = datetime.max if isinstance(value, datetime) else date.max
            inverted_value = max_date - value
            return (True, inverted_value)
        else:
            return (True, value)
    else:
        return (True, value)


def validate_and_sort_records(
    raw_records: List[Dict[str, Any]], Model: Any, sort_keys: List[str]
) -> List[Dict[str, Any]]:
    """
    Validate and sort a list of raw records based on specified sorting keys.

    Each record is validated against a provided model class, ensuring data consistency.
    The function also handles custom sorting logic, including handling of None values
    and conversion of date strings into datetime objects for accurate sorting.

    Parameters:
    - raw_records (List[Dict[str, Any]]): A list of dictionaries representing the raw records.
    - Model (Any): A class used for data validation and conversion, typically a Pydantic model.
    - sort_keys (List[str]): Keys based on which the records will be sorted. A key prefixed
                             with "-" indicates reverse sorting for that key.

    Returns:
    - List[Dict[str, Any]]: A list of validated and sorted dictionaries.

    Note:
    - The function assumes that `Model` has a method `template_representation` that converts
      the model instance into a dictionary suitable for further processing.
    """

    temp_records = []

    for raw_record in raw_records:
        # Validate each record using the provided model
        model_instance = Model(**raw_record)
        model_dict = model_instance.template_representation()

        # Prepare for sorting by extracting relevant values
        # and converting date strings into datetime objects
        sort_values = {key: model_dict.get(key) for key in sort_keys}
        for key in ["score_date", "start_date"]:
            if key in sort_keys:
                value = sort_values[key]
                if value and isinstance(value, str):
                    try:
                        sort_values[key] = datetime.strptime(value, "%b %d, %Y")
                    except ValueError:
                        # Handle incorrect date format
                        pass

        temp_records.append((sort_values, model_dict))

    # Define a composite key function for sorting
    def composite_sort_key(item):
        sort_values = []
        for key in sort_keys:
            reverse = key.startswith("-")
            actual_key = key[1:] if reverse else key
            value = item[0].get(actual_key, item[1].get(actual_key, ""))
            sort_value = none_safe_key(value, reverse)
            if reverse:
                sort_values.append((-sort_value[0], sort_value[1]))
            else:
                sort_values.append(sort_value)
        return tuple(sort_values)

    # Sorting Logic:
    # The composite_sort_key function generates a tuple of sorting values for each record.
    # This tuple is based on all the sort keys provided, handling reverse sorting as needed.
    # The sort function uses these tuples to sort the records in the desired order.
    temp_records.sort(key=composite_sort_key)

    # Extract and return the original records
    processed_records = [record for _, record in temp_records]
    return processed_records

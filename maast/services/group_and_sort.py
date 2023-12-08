from typing import List, Dict, Any
from collections import defaultdict


def group_and_sort(
    data: List[Dict[str, Any]],
    group_by_key: str,
    subgroup_sort_keys: List[str],
    sort_orders: List[bool] = None,
) -> Dict[str, List[Dict[str, Any]]]:
    if sort_orders is None:
        sort_orders = [True] * len(subgroup_sort_keys)  # Default to ascending sort

    grouped_data = defaultdict(list)
    for item in data:
        group_key = item[group_by_key]
        grouped_data[group_key].append(item)

    # Sort each subgroup with multiple sort keys
    for group in grouped_data:
        grouped_data[group].sort(
            key=lambda x: tuple(x[key] for key in subgroup_sort_keys),
            reverse=not all(sort_orders),
        )

    # Convert to regular dict and sort groups
    return dict(sorted(grouped_data.items()))


def sort_data(
    data: List[Dict[str, Any]], sort_keys: List[str], sort_orders: List[bool] = None
) -> List[Dict[str, Any]]:
    """
    Sorts the given data based on the specified sort keys and sort orders.

    Args:
        data (List[Dict[str, Any]]): The data to be sorted.
        sort_keys (List[str]): The keys to sort the data by. The data will be sorted in the order of these keys.
        sort_orders (List[bool], optional): The sort orders for each sort key. If not provided, defaults to ascending sort for all keys.

    Returns:
        List[Dict[str, Any]]: The sorted data.

    """
    if sort_orders is None:
        sort_orders = [True] * len(sort_keys)  # Default to ascending sort
    data.sort(
        key=lambda item: tuple(item[key] for key in sort_keys),
        reverse=not all(sort_orders),
    )
    return data

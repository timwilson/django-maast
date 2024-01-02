from django.http import HttpResponsePermanentRedirect
from urllib.parse import unquote, quote


def redirect_old_individual_rankings(request):
    round_id = request.GET.get("r", "")
    division = unquote(request.GET.get("d", ""))  # Decode division for processing

    # Find the position of 'Male' or 'Female' in the division
    gender = "Male" if "Male" in division else "Female"
    gender_index = division.index(gender)

    # Extract and re-encode age_division and equipment_class
    age_division = quote(division[:gender_index].rstrip())
    equipment_class = quote(division[gender_index + len(gender) :].lstrip())

    # Construct the new URL
    new_url = f"/scores/{round_id}?age_division={age_division}&gender={quote(gender)}&equipment_class={equipment_class}"

    return HttpResponsePermanentRedirect(new_url)

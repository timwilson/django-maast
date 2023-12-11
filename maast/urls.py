from django.urls import path

from maast.views.events import get_valid_scores_by_event
from maast.views.organizations import organizations_view
from maast.views.persons import get_valid_data_by_person
from maast.views.records import get_valid_records_by_round
from maast.views.scores import get_valid_scores_by_round_and_division

urlpatterns = [
    # path("", home_page_view, name="home"),
    path("organizations", organizations_view, name="organization_records"),
    path("profile/<str:person_slug>", get_valid_data_by_person, name="person_profile"),
    path("records/<int:round_id>", get_valid_records_by_round, name="round_records"),
    path(
        "scores/<int:round_id>",
        get_valid_scores_by_round_and_division,
        name="round_scores_by_division",
    ),
    path("event/<int:event_id>", get_valid_scores_by_event, name="event_scores"),
]

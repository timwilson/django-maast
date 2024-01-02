from django.contrib.sitemaps.views import sitemap
from django.urls import path

from maast.sitemaps import PersonSitemap
from maast.views.events import get_valid_scores_by_event, get_valid_events
from maast.views.home import home_page_view
from maast.views.persons import (
    get_valid_data_by_person,
    get_valid_person_scores,
    get_valid_person_podiums,
    get_valid_person_state_records,
    search_persons_by_name,
)
from maast.views.records import get_valid_records_by_round
from maast.views.redirects import redirect_old_individual_rankings
from maast.views.scores import get_valid_scores_by_round_and_division

sitemaps = {
    "persons": PersonSitemap,
}

urlpatterns = [
    path("", home_page_view, name="home"),
    path("profile/<str:person_slug>", get_valid_data_by_person, name="person_profile"),
    path("records/<int:round_id>", get_valid_records_by_round, name="round_records"),
    path(
        "scores/<int:round_id>",
        get_valid_scores_by_round_and_division,
        name="round_scores_by_division",
    ),
    path("event/<int:event_id>", get_valid_scores_by_event, name="event_scores"),
    path("events", get_valid_events, name="event_list"),
    path("api/scores/<int:person_id>", get_valid_person_scores, name="api_scores"),
    path(
        "api/records/<int:person_id>",
        get_valid_person_state_records,
        name="api_records",
    ),
    path("api/podiums/<int:person_id>", get_valid_person_podiums, name="api_podiums"),
    path("api/search", search_persons_by_name, name="api_person_search"),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    path(
        "individual_rankings.php",
        redirect_old_individual_rankings,
        name="redirect_old_individual_rankings",
    ),
]

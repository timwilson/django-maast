from django.urls import path

from maast.views.organizations import organizations_view
from maast.views.records import get_valid_records_by_round

urlpatterns = [
    # path("", home_page_view, name="home"),
    path("organizations", organizations_view, name="organization_records"),
    path("records/<int:round_id>", get_valid_records_by_round, name="round_records"),
]

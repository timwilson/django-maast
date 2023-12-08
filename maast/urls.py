from django.urls import path

from maast.views.organizations import organizations_view
from maast.views.records import records_by_round_view

urlpatterns = [
    # path("", home_page_view, name="home"),
    path("organizations", organizations_view, name="organization_records"),
    path("records/<int:round_id>", records_by_round_view, name="round_records"),
]

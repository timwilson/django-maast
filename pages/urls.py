from django.urls import path
from .views import (
    RobotsTxtView,
    PrivacyView,
    TermsView,
    FAQView,
    EquipmentClassesView,
    AgeDivisionsView,
    RoundsView,
)

urlpatterns = [
    path("robots.txt", RobotsTxtView.as_view(content_type="text/plain"), name="robots"),
    path("faq", FAQView.as_view(), name="faq"),
    path("privacy", PrivacyView.as_view(), name="privacy"),
    path("terms-of-use", TermsView.as_view(), name="terms-of-use"),
    path("equipment-classes", EquipmentClassesView.as_view(), name="equipment-classes"),
    path("age-divisions", AgeDivisionsView.as_view(), name="age-divisions"),
    path("rounds", RoundsView.as_view(), name="rounds"),
]

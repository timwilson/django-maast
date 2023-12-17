from django.views.generic import TemplateView


class RobotsTxtView(TemplateView):
    template_name = "robots.txt"


class TestFileView(TemplateView):
    template_name = "test.html"


class FAQView(TemplateView):
    template_name = "faq.html"


class PrivacyView(TemplateView):
    template_name = "privacy_policy.html"


class TermsView(TemplateView):
    template_name = "terms_of_use.html"

from django.views.generic import TemplateView
from meta.views import Meta


class RobotsTxtView(TemplateView):
    template_name = "robots.txt"


class FAQView(TemplateView):
    template_name = "faq.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["meta"] = Meta(
            title="FAQs — MAA Score Tabulator",
            site_name="MAA Score Tabulator",
            description="Frequently asked questions (FAQs) about the MAA Score Tabulator state record database",
            url="/faq",
            image_object={
                "url": "https://records/themnaa.org/static/img/MAAST-og.png",
                "type": "image/png",
                "width": 1200,
                "height": 628,
                "alt": "MAAST: State record and score database",
            },
            keywords=["FAQ", "questions", "answers"],
        )
        return context


class PrivacyView(TemplateView):
    template_name = "privacy_policy.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["meta"] = Meta(
            title="Privacy Policy — MAA Score Tabulator",
            site_name="MAA Score Tabulator",
            description="Privacy policy for the MAA Score Tabulator state record database",
            url="/privacy",
            image_object={
                "url": "https://records/themnaa.org/static/img/MAAST-og.png",
                "type": "image/png",
                "width": 1200,
                "height": 628,
                "alt": "MAAST: State record and score database",
            },
            keywords=["privacy", "privacy policy"],
        )
        return context


class TermsView(TemplateView):
    template_name = "terms_of_use.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["meta"] = Meta(
            title="Terms of Use — MAA Score Tabulator",
            site_name="MAA Score Tabulator",
            description="Terms of Use for the MAA Score Tabulator state record database",
            url="/terms-of-use",
            image_object={
                "url": "https://records/themnaa.org/static/img/MAAST-og.png",
                "type": "image/png",
                "width": 1200,
                "height": 628,
                "alt": "MAAST: State record and score database",
            },
            keywords=["terms of use"],
        )
        return context

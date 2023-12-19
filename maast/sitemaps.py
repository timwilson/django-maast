from django.contrib.sitemaps import Sitemap

from maast.models import Person
from maast.services.http_client import MaastHTTPClient
from maast_web import settings


class PersonSitemap(Sitemap):
    """
    A class representing a sitemap for persons.

    Inherits from: Sitemap

    Methods:
        - items(): Returns a list of persons available.
        - location(obj): Returns the URL location of a person.

    """

    def items(self):
        client = MaastHTTPClient()  # Your custom HTTP client
        response = client.get(f"{settings.API_HOST}/v1/persons")
        response.raise_for_status()
        person_data = response.json()
        persons = [Person(**data) for data in person_data]
        return persons

    def location(self, obj):
        return f"/profile/{obj.slug}"

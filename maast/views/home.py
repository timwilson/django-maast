from django.shortcuts import render
from meta.views import Meta
from blog.models import SiteUpdateBlog
from maast_web import settings


def home_page_view(request):
    meta = Meta(
        title="MAA Score Tabulator — Home",
        site_name="MAA Score Tabulator",
        description="State records and complete score history for Minnesota Archers Alliance events since 2003",
        url="/",
        image_object={
            "url": f"{settings.SITE_DOMAIN}/static/img/MAAST-og.png",
            "type": "image/png",
            "width": 1200,
            "height": 628,
            "alt": "MAAST: State record and score database",
        },
    )
    # Get the site updates from the database
    posts = SiteUpdateBlog.objects.filter(is_draft=False).order_by("-published_date")

    return render(request, "home.html", {"posts": posts, "meta": meta})

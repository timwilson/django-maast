from django.shortcuts import render

from blog.models import SiteUpdateBlog


def home_page_view(request):
    # Get the site updates from the database
    posts = SiteUpdateBlog.objects.filter(is_draft=False).order_by("-published_date")

    return render(request, "home.html", {"posts": posts})

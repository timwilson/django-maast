from django.contrib import admin

from blog.models import SiteUpdateBlog


class SiteUpdateBlogAdmin(admin.ModelAdmin):
    model = SiteUpdateBlog
    list_display = [
        "headline",
        "body",
        "is_draft",
        "published_date",
    ]


admin.site.register(SiteUpdateBlog, SiteUpdateBlogAdmin)

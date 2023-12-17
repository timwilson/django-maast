from django.db import models
from django.utils import timezone


class SiteUpdateBlog(models.Model):
    headline = models.CharField(max_length=200)
    body = models.TextField()
    is_draft = models.BooleanField(default=True)
    published_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = "Site Update"

    def publish(self):
        self.published_date = timezone.now()
        self.is_draft = False
        self.save()

    def __str__(self):
        return self.headline

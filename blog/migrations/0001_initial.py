# Generated by Django 5.0 on 2023-12-15 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SiteUpdateBlog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headline', models.CharField(max_length=200)),
                ('body', models.TextField()),
                ('is_draft', models.BooleanField(default=True)),
                ('published_date', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]

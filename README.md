# MAA Score Database Website

The [MAA Score Database](https://records.themnaa.org/) is created in Django and draws its data from the [MAAST-API](https://api.themnaa.org/) which is based on FastAPI. The data is stored in a SQLite database.

## Building the site

When working on the site, the `django-browser-reload` plugin will automatically rebuild the site as you make changes when running in DEBUG mode.

The site is styled with TailwindCSS using the [Django-Tailwind](https://django-tailwind.readthedocs.io/en/latest/index.html) package. In order to have the Tailwind styles build automatically during site editing, start development mode using:

`python manage.py tailwind start`

Before the final project build, it's necessary to build the tailwind styles in a way that can be collected into the static folder.

`python manage.py tailwind build`

Finally, don't forget to collect the static files.

`python manage.py collectstatic`
from .celery import app as celery_app

# Adding the celery.py module into the django project to ensure it loads when django starts.
__all__: list([str, ...]) = [
    'celery_app',
]

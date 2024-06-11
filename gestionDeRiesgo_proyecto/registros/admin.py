from django.contrib import admin
from django.apps import apps

app_models = apps.get_app_config('registros').get_models()

for model in app_models:
    try:
        admin.site.register(model)
    except admin.site.register(model):
        pass


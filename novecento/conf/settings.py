from django.conf import settings

USE_FILEBROWSER = getattr(settings, "NOVECENTO_USE_FILEBROWSER", False)
USE_DJANGO_MULTILINGUAL = getattr(settings, "NOVECENTO_USE_DJANGO_MULTILINGUAL", False)
USE_DJANGO_PAGINATION = getattr(settings, "NOVECENTO_USE_DJANGO_PAGINATION", False)    

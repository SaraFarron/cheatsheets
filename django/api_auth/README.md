### Dependencies:

    Django
    djangorestframework

### Add to settings.py

    REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
            'rest_framework.permissions.IsAdminUser'
    ),
    }

    INSTALLED_APPS = [
        ...
        'rest_framework.authtoken',
    ]
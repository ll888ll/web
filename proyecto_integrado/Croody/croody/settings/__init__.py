# ========================================
# Settings Package
# ========================================
# Import the appropriate settings based on DJANGO_SETTINGS_MODULE
# Default to development settings if not specified
import os

settings_module = os.getenv('DJANGO_SETTINGS_MODULE', 'croody.settings.development')

if settings_module in ('croody.settings.development', 'croody.settings'):
    from .development import *
elif settings_module == 'croody.settings.production':
    from .production import *
elif settings_module == 'croody.settings.base':
    from .base import *
else:
    # Default to development for unknown values
    from .development import *

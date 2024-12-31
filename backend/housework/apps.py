from django.apps import AppConfig
from django.core.management import call_command

class HouseworkConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'housework'

    def ready(self):
        # Run migrations first
        call_command('ensure_migrations')
        
        # Import and run the bucket initialization
        from .utils import ensure_minio_bucket
        ensure_minio_bucket()
        
        # Ensure superuser exists
        call_command('ensure_superuser')

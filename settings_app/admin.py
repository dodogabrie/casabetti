from django.contrib import admin
from .models import SiteSettings


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Only allow one instance
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Prevent deletion
        return False

    fieldsets = (
        ('Informazioni Generali', {
            'fields': ('site_title',),
            'description': 'Configurazione generale del sito'
        }),
        ('Home Page', {
            'fields': ('home_welcome_title', 'home_intro_text', 'home_background_image'),
            'description': 'Contenuti visualizzati nella pagina home'
        }),
        ('Aspetto Visivo', {
            'fields': ('header_background_image',),
            'description': 'Configura l\'aspetto visivo del sito'
        }),
    )

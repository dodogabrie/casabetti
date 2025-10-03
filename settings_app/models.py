from django.db import models
from filer.fields.image import FilerImageField


class SiteSettings(models.Model):
    """Singleton model for site-wide settings"""
    site_title = models.CharField(
        max_length=100,
        default="Casa Betti",
        verbose_name="Titolo del Sito",
        help_text="Titolo visualizzato nell'intestazione del sito"
    )
    header_background_image = FilerImageField(
        null=True,
        blank=True,
        related_name="site_header_background",
        on_delete=models.SET_NULL,
        verbose_name="Immagine di sfondo intestazione",
        help_text="Immagine di sfondo per l'intestazione del sito. Se non impostata, verrà usato il colore marrone di default."
    )

    class Meta:
        verbose_name = "Impostazioni Sito"
        verbose_name_plural = "Impostazioni Sito"

    def __str__(self):
        return "Impostazioni Sito"

    def save(self, *args, **kwargs):
        # Ensure only one instance exists (singleton pattern)
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Prevent deletion
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

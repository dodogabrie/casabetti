from django.db import models
from filer.fields.image import FilerImageField


class Item(models.Model):
    CATEGORY_CHOICES = [
        ("furniture", "Mobili"),
        ("electronics", "Elettronica"),
        ("clothing", "Abbigliamento"),
        ("books", "Libri"),
        ("sports", "Sport"),
        ("other", "Altro"),
        ("paintings", "Dipinti"),
        ("fancy-goods", "Oggettistica"),
    ]

    STATUS_CHOICES = [
        ("available", "Disponibile"),
        ("reserved", "Riservato"),
        ("sold", "Venduto"),
    ]

    title = models.CharField(max_length=200, verbose_name="Titolo")
    description = models.TextField(verbose_name="Descrizione")
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Prezzo (€)"
    )
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default="other",
        verbose_name="Categoria",
    )
    year = models.PositiveIntegerField(verbose_name="Anno", null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="available", verbose_name="Stato"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creato il")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Aggiornato il")

    class Meta:
        verbose_name = "Articolo"
        verbose_name_plural = "Articoli"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    @property
    def main_image(self):
        return self.images.first()


class ItemImage(models.Model):
    item = models.ForeignKey(Item, related_name="images", on_delete=models.CASCADE)
    image = FilerImageField(
        null=True,
        blank=True,
        related_name="item_images",
        on_delete=models.CASCADE,
        verbose_name="Immagine",
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Ordine")

    class Meta:
        verbose_name = "Immagine Articolo"
        verbose_name_plural = "Immagini Articolo"
        ordering = ["order"]

    def __str__(self):
        return f"Immagine per {self.item.title}"

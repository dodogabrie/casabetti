from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from items.models import Item, ItemImage
from filer.models import File as FilerFile, Image as FilerImage
from PIL import Image, ImageDraw, ImageFont
import io
import random


class Command(BaseCommand):
    help = 'Popola la bacheca con 5 articoli di esempio con gallerie di immagini'

    def handle(self, *args, **kwargs):
        # Clear existing items
        self.stdout.write('Rimozione articoli esistenti...')
        Item.objects.all().delete()

        sample_items = [
            {
                'title': 'Divano in pelle marrone',
                'description': 'Divano a tre posti in vera pelle marrone, ottimo stato. Dimensioni: 200x90x85 cm. Molto comodo e perfetto per il salotto.',
                'price': '450.00',
                'category': 'furniture',
                'colors': ['#8B4513', '#A0522D', '#654321'],
            },
            {
                'title': 'Laptop Dell XPS 13',
                'description': 'Laptop Dell XPS 13 del 2022, processore Intel i7, 16GB RAM, SSD 512GB. Ottime condizioni, poco usato. Include caricatore originale.',
                'price': '850.00',
                'category': 'electronics',
                'colors': ['#C0C0C0', '#808080', '#696969'],
            },
            {
                'title': 'Giacca di jeans Levi\'s',
                'description': 'Giacca di jeans classica Levi\'s, taglia M. Blu scuro, in buonissime condizioni. Perfetta per la mezza stagione.',
                'price': '45.00',
                'category': 'clothing',
                'colors': ['#1E3A8A', '#2563EB', '#3B82F6'],
            },
            {
                'title': 'Collezione libri Harry Potter',
                'description': 'Collezione completa dei 7 libri di Harry Potter in italiano. Edizione brossura, ottime condizioni. Ideale regalo per appassionati.',
                'price': '65.00',
                'category': 'books',
                'colors': ['#7C2D12', '#DC2626', '#FCD34D'],
            },
            {
                'title': 'Bicicletta da corsa Bianchi',
                'description': 'Bici da corsa Bianchi, telaio in alluminio, cambio Shimano 21 velocità. Taglia 54, ruote 28". Perfettamente funzionante.',
                'price': '320.00',
                'category': 'sports',
                'colors': ['#06B6D4', '#0891B2', '#0E7490'],
            },
        ]

        for item_data in sample_items:
            self.stdout.write(f"Creazione: {item_data['title']}...")

            # Create item
            colors = item_data.pop('colors')
            item = Item.objects.create(**item_data)

            # Create 3-5 sample images for each item
            num_images = random.randint(3, 5)
            for i in range(num_images):
                image = self.create_sample_image(
                    item_data['title'],
                    colors[i % len(colors)],
                    i + 1
                )

                # Save to filer
                image_bytes = io.BytesIO()
                image.save(image_bytes, format='JPEG')
                image_bytes.seek(0)

                # Create FilerImage
                filer_image = FilerImage(
                    owner=None,
                    original_filename=f"{item.title.lower().replace(' ', '_')}_{i+1}.jpg",
                    file=ContentFile(image_bytes.read(), name=f"sample_{item.id}_{i+1}.jpg")
                )
                filer_image.save()

                # Create ItemImage
                ItemImage.objects.create(
                    item=item,
                    image=filer_image,
                    order=i
                )

            self.stdout.write(
                self.style.SUCCESS(f'✓ Creato "{item.title}" con {num_images} immagini')
            )

        self.stdout.write(
            self.style.SUCCESS(f'\n✓ Bacheca popolata con successo: {len(sample_items)} articoli creati!')
        )

    def create_sample_image(self, title, color, number):
        """Create a sample colored image with text"""
        width, height = 800, 600
        image = Image.new('RGB', (width, height), color=color)
        draw = ImageDraw.Draw(image)

        # Add text
        text = f"{title}\n#{number}"

        # Try to use a font, fallback to default
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 40)
        except:
            font = ImageFont.load_default()

        # Calculate text position (centered)
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        position = ((width - text_width) // 2, (height - text_height) // 2)

        # Add semi-transparent overlay
        overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        overlay_draw.rectangle(
            [(position[0] - 20, position[1] - 20),
             (position[0] + text_width + 20, position[1] + text_height + 20)],
            fill=(255, 255, 255, 180)
        )
        image = Image.alpha_composite(image.convert('RGBA'), overlay).convert('RGB')

        # Draw text on image
        draw = ImageDraw.Draw(image)
        draw.text(position, text, fill='black', font=font)

        return image

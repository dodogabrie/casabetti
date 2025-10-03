from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Item


def item_list(request):
    items = Item.objects.filter(status='available').prefetch_related('images')

    category = request.GET.get('category')
    search = request.GET.get('search')

    if category:
        items = items.filter(category=category)

    if search:
        items = items.filter(title__icontains=search)

    return render(request, 'items/item_list.html', {
        'items': items,
        'categories': Item.CATEGORY_CHOICES,
        'current_category': category,
        'search_query': search,
    })


def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    return render(request, 'items/item_detail.html', {
        'item': item,
    })


def item_list_api(request):
    items = Item.objects.filter(status='available').prefetch_related('images')

    category = request.GET.get('category')
    search = request.GET.get('search')

    if category:
        items = items.filter(category=category)

    if search:
        items = items.filter(title__icontains=search)

    data = []
    for item in items:
        main_image = item.main_image
        data.append({
            'id': item.id,
            'title': item.title,
            'description': item.description,
            'price': str(item.price),
            'category': item.get_category_display(),
            'main_image_url': main_image.image.url if main_image and main_image.image else None,
            'main_image_thumbnail': main_image.image.easy_thumbnails_thumbnailer.get_thumbnail({
                'size': (300, 300),
                'crop': True
            }).url if main_image and main_image.image else None,
            'images_count': item.images.count(),
        })

    return JsonResponse({'items': data})

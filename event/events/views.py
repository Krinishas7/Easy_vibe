from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Event, Category


def home_view(request):
    """Home page with featured events"""
    featured_events = Event.objects.filter(
        status='published'
    ).order_by('-created_at')[:6]
    
    categories = Category.objects.all()[:6]
    
    context = {
        'featured_events': featured_events,
        'categories': categories,
        'title': 'Home'
    }
    return render(request, 'events/home.html', context)


def event_list_view(request):
    """List all published events with filtering and pagination"""
    events = Event.objects.filter(status='published').order_by('-created_at')
    categories = Category.objects.all()
    
    # Filtering
    category_id = request.GET.get('category')
    search_query = request.GET.get('search')
    
    selected_category_name = None
    if category_id:
        events = events.filter(category_id=category_id)
        try:
            selected_category_name = Category.objects.get(id=category_id).name
        except Category.DoesNotExist:
            pass
    
    if search_query:
        events = events.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(venue__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(events, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': int(category_id) if category_id else None,
        'selected_category_name': selected_category_name,
        'search_query': search_query,
        'title': 'Events'
    }
    return render(request, 'events/event_list.html', context)


def event_detail_view(request, slug):
    """Event detail page"""
    event = get_object_or_404(Event, slug=slug, status='published')
    
    # Get related events
    related_events = Event.objects.filter(
        category=event.category,
        status='published'
    ).exclude(id=event.id)[:4]
    
    context = {
        'event': event,
        'related_events': related_events,
        'title': event.title
    }
    return render(request, 'events/event_detail.html', context)

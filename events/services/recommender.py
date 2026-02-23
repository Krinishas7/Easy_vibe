from django.db.models import Count
from ..models import Event

def get_personalized_recommendations(user, limit=6):
    """
    Finds events based on the user's booking history categories.
    """
    if not user.is_authenticated:
        return Event.objects.filter(status='published').order_by('-created_at')[:limit]

    # Get categories the user has interacted with
    booked_categories = Event.objects.filter(
        bookings__user=user
    ).values_list('category', flat=True).distinct()

    if not booked_categories:
        # Fallback: Top trending events if user has no history
        return Event.objects.filter(status='published').annotate(
            bc=Count('bookings')).order_by('-bc')[:limit]

    # Recommend events in those categories the user hasn't booked yet
    return Event.objects.filter(
        category__in=booked_categories,
        status='published'
    ).exclude(bookings__user=user).distinct()[:limit]
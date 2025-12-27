from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Category, Event, SeatType


# -------------------------
# CATEGORY ADMIN
# -------------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'event_count', 'created_at']
    search_fields = ['name', 'description']
    list_filter = ['created_at']

    def event_count(self, obj):
        count = obj.events.count()
        if count > 0:
            url = reverse('admin:events_event_changelist') + f'?category__id__exact={obj.id}'
            return format_html('<a href="{}">{} events</a>', url, count)
        return '0 events'


# -------------------------
# SEAT TYPES INLINE
# -------------------------
class SeatTypeInline(admin.TabularInline):
    model = SeatType
    extra = 1
    fields = ('name', 'price', 'total_seats', 'seats_available')
    readonly_fields = ('seats_available',)


# -------------------------
# EVENT ADMIN
# -------------------------
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'category', 'organizer', 'venue', 'start_date',
        'status', 'tickets_sold_display', 'revenue_display', 'image_preview'
    ]

    list_filter = ['status', 'category', 'start_date', 'created_at']
    search_fields = ['title', 'description', 'venue', 'organizer__username']
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['-created_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description', 'category', 'organizer', 'status'),
        }),
        ('Event Details', {
            'fields': ('venue', 'address', 'start_date', 'end_date', 'image'),
        }),

        # -----------------------------
        # COUNTRY SETTINGS (ADMIN)
        # -----------------------------
        ('Location / Country', {
            'fields': (
                'country',
                'allow_any_country',
            ),
        }),
        # -----------------------------

        ('Venue Coordinates (Optional)', {
            'fields': ('latitude', 'longitude', 'map_preview'),
        }),

        ('Ticketing', {
            'fields': ('total_tickets', 'available_tickets', 'price'),
        }),
    )

    readonly_fields = ['available_tickets', 'map_preview']
    inlines = [SeatTypeInline]

    # ------------------------------------------------------
    # LOCATION MAP (UNCHANGED)
    # ------------------------------------------------------
    def map_preview(self, obj):
        return mark_safe("""
            <style>
                #location-map {
                    height: 320px;
                    border-radius: 10px;
                    margin-top: 10px;
                    border: 1px solid #ddd;
                }
            </style>

            <link rel="stylesheet"
                  href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>

            <div id="location-map"></div>
            <small style="color:#888;">
                Drag the marker or click on the map to set the event venue location.
            </small>

            <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

            <script>
            (function() {
                function initEventVenueMap() {
                    var mapDiv = document.getElementById("location-map");
                    if (!mapDiv || typeof L === "undefined") return;

                    var latInput = document.getElementById("id_latitude");
                    var lngInput = document.getElementById("id_longitude");
                    if (!latInput || !lngInput) return;

                    var lat = parseFloat(latInput.value);
                    var lng = parseFloat(lngInput.value);

                    if (isNaN(lat) || isNaN(lng)) {
                        lat = 27.700769;
                        lng = 85.300140;
                    }

                    var map = L.map(mapDiv).setView([lat, lng], 13);

                    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
                        maxZoom: 19
                    }).addTo(map);

                    var marker = L.marker([lat, lng], { draggable: true }).addTo(map);

                    function updateInputs(pos) {
                        latInput.value = pos.lat.toFixed(6);
                        lngInput.value = pos.lng.toFixed(6);
                    }

                    marker.on("dragend", function(e) {
                        updateInputs(e.target.getLatLng());
                    });

                    map.on("click", function(e) {
                        marker.setLatLng(e.latlng);
                        updateInputs(e.latlng);
                    });
                }

                if (document.readyState === "complete" || document.readyState === "interactive") {
                    setTimeout(initEventVenueMap, 50);
                } else {
                    document.addEventListener("DOMContentLoaded", initEventVenueMap);
                }
            })();
            </script>
        """)

    map_preview.short_description = "Venue Location"

    # ------------------------------------------------------
    # DISPLAY HELPERS
    # ------------------------------------------------------
    def tickets_sold_display(self, obj):
        sold = obj.tickets_sold
        total = obj.total_tickets
        pct = (sold / total * 100) if total > 0 else 0
        color = 'green' if pct > 70 else 'orange' if pct > 30 else 'red'
        return format_html(
            '<span style="color:{};">{}/{} ({}%)</span>',
            color, sold, total, round(pct, 1)
        )

    def revenue_display(self, obj):
        revenue = obj.tickets_sold * obj.price
        return f"Rs. {revenue:,.2f}"

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit:cover; border-radius:5px;" />',
                obj.image.url
            )
        return "No image"

    # ------------------------------------------------------
    # ACTIONS
    # ------------------------------------------------------
    actions = ['make_published', 'make_draft', 'make_cancelled']

    def make_published(self, request, queryset):
        queryset.update(status='published')

    def make_draft(self, request, queryset):
        queryset.update(status='draft')

    def make_cancelled(self, request, queryset):
        queryset.update(status='cancelled')

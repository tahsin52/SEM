from django.contrib import admin

from core.models import CarModel


class CarModelAdmin(admin.ModelAdmin):
    list_display = ('make', 'transmission', 'year', 'created_at', 'updated_at')
    list_display_links = ('make',)
    search_fields = ('make', 'transmission', 'year')
    list_per_page = 100


admin.site.register(CarModel, CarModelAdmin)
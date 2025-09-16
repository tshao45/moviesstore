from django.contrib import admin
from .models import Movie, Review

class MovieAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.amount_left == 0:
            return self.readonly_fields + ("amount_left",)
        return self.readonly_fields
admin.site.register(Movie, MovieAdmin)
admin.site.register(Review)
# Register your models here.

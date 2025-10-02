from django.contrib import admin
from .models import Movie, Review, Petition

class MovieAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name']

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.amount_left == 0:
            return self.readonly_fields + ("amount_left",)
        return self.readonly_fields
admin.site.register(Movie, MovieAdmin)
admin.site.register(Review)
admin.site.register(Petition)

class PetitionAdmin(admin.ModelAdmin):
    list_display = ('movie_name', 'user', 'votes', 'date')  # Columns shown in admin
    search_fields = ('movie_name', 'description', 'user__username')  # Allow search
    list_filter = ('date',)  # Filter by date
    ordering = ('-date',)  # Newest first

# Register your models here.

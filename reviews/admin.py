from django.contrib import admin
from .models import Mineral_Water,Review


class ReviewAdmin(admin.ModelAdmin):
    model = Review
    list_display = ('mineralwater','user_name','comment','pub_date')
    list_filter = ['pub_date', 'user_name']
    search_fields = ['comment']

admin.site.register(Mineral_Water)
admin.site.register(Review, ReviewAdmin)



from django.contrib import admin
from .models import Book, Purchase

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'price', 'created_at')
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Purchase)
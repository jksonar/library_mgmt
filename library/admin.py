from django.contrib import admin
from .models import Book, Category, Issue

# admin.site.register(Book)
admin.site.register(Category)
admin.site.register(Issue)

class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'quantity')
    search_fields = ('title', 'tags')  # to search by tags

admin.site.register(Book, BookAdmin)

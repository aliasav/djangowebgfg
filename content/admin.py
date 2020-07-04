"""Django admin config for content app
"""
from django.contrib import admin
from content.models import VocabItem


class VocabItemAdmin(admin.ModelAdmin):
    """
    Modeladmin for VocabItem
    """
    list_display = ("word", "meaning", "pos", "created_at", "updated_at")
    search_fields = ["guid", "word"]
    readonly_fields = ['sentences', 'created_at', 'updated_at',]

admin.site.register(VocabItem, VocabItemAdmin)

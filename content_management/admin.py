from django.contrib import admin
from .models import Content

# admin.site.register(Content)
@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "category",
        "difficulty",
        "status",
        "is_published",
        "author",
        "view_count",
        "created_at",
    ]

    list_filter = [
        "difficulty",
        "status",
        "is_published",
        "category",
    ]

    search_fields = [
        "title",
        "body",
    ]

    ordering = [
        "-created_at"
    ]

    filter_horizontal = [
        "tags"
    ]

    readonly_fields = [
        "created_at",
        "updated_at"
    ]

    @admin.display(description="Views")
    def view_count(self, obj):
        return obj.views.count()



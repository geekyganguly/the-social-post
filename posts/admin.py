from django.contrib import admin
from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'updated_date',
                    'get_likes_count', 'is_public', 'user',)


admin.site.register(Post, PostAdmin)

from django.contrib import admin

from .models import Post, Category, Tag, Contact, Comment


class CategoryInline(admin.TabularInline):
    model = Post
    extra = 1
    fields = ('id', 'title', 'subject', 'is_published')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'image', 'is_published', 'views_count', 'created_at')
    list_display_links = ('id', 'title')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    list_display_links = ('id', 'name', 'created_at')
    inlines = (CategoryInline,)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    list_display_links = ('id', 'name')


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_solved', 'created_at')
    list_display_links = ('name', 'created_at')


@admin.register(Comment)
class Comment(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
    list_display_links = ('name', 'created_at')

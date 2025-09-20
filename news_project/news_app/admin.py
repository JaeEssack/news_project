from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import CustomUser, Publisher, Article


# Custom User Admin
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'role')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
        ('Subscriptions', {'fields': ('subscribed_publishers', 'subscribed_journalists')}),
        ('Journalist Info', {'fields': ('bio', 'published_articles')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)


# Publisher Admin
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

admin.site.register(Publisher, PublisherAdmin)


# Article Admin
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'publisher', 'journalist', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'publisher', 'journalist')
    search_fields = ('title', 'content')
    actions = ['approve_articles']

    # Custom action to approve selected articles
    def approve_articles(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f"{updated} article(s) successfully approved.")
    approve_articles.short_description = "Approve selected articles"

admin.site.register(Article, ArticleAdmin)

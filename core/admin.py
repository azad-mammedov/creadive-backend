from django import forms
from django.contrib import admin
from django.utils.html import format_html_join, format_html
from modeltranslation.admin import TranslationAdmin

from .models import (
    BlogPost,
    PortfolioItem,
    Service,
    TeamMember,
    Testimonial,
    ContactInquiry,
    Tag,
    Technology,
    ServiceFeature,
    SocialLink,
)


# --- Inline Admin Classes ---
class ServiceFeatureInline(admin.TabularInline):
    """Inline admin for service features"""
    model = ServiceFeature
    extra = 1
    ordering = ['order', 'id']
    
    def get_queryset(self, request):
        """Optimize inline queryset"""
        return super().get_queryset(request).select_related('service')


class SocialLinkInline(admin.TabularInline):
    """Inline admin for social links"""
    model = SocialLink
    extra = 1
    ordering = ['order', 'id']
    
    def get_queryset(self, request):
        """Optimize inline queryset"""
        return super().get_queryset(request).select_related('team_member')


# --- Shared Admin Mixins ---
class TimeStampedAdmin(admin.ModelAdmin):
    """Base admin class for timestamped models"""
    readonly_fields = ("createdAt", "updatedAt")
    ordering = ("-createdAt",)


class OrderedAdmin(admin.ModelAdmin):
    """Base admin class for ordered models"""
    readonly_fields = ("createdAt", "updatedAt")
    ordering = ("order", "id")


class RelationshipDisplayMixin:
    """Mixin for displaying related objects"""
    def render_related_list(self, obj, related_manager, field_name='name'):
        """Render a list of related objects"""
        items = related_manager.all()
        if not items:
            return "-"
        values = [getattr(item, field_name) for item in items]
        return format_html_join(", ", "{}", ((v,) for v in values))
    
    def render_social_links(self, obj):
        """Render social links as formatted list"""
        links = obj.social_links.all()
        if not links:
            return "-"
        items = [f"<b>{link.get_platform_display()}</b>: {link.url}" for link in links]
        return format_html("<br>".join(items))


# --- Admin Registrations for New Models ---
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Admin for Tag model"""
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    """Admin for Technology model"""
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)


# --- Admin Registrations for Main Models ---

@admin.register(BlogPost)
class BlogPostAdmin(TranslationAdmin, TimeStampedAdmin, RelationshipDisplayMixin):
    """Admin for BlogPost model"""
    list_display = ("id", "title", "category", "status", "date", "author", "tags_display")
    list_filter = ("status", "category", "date", "author", "tags")
    search_fields = ("title", "excerpt", "content", "category")
    autocomplete_fields = ("author",)
    filter_horizontal = ("tags",)
    date_hierarchy = "date"
    
    def get_queryset(self, request):
        """Optimize queryset to prevent N+1 queries"""
        return super().get_queryset(request).select_related('author').prefetch_related('tags')

    def tags_display(self, obj):
        return self.render_related_list(obj, obj.tags)
    tags_display.short_description = "Tags"


@admin.register(PortfolioItem)
class PortfolioItemAdmin(TranslationAdmin, TimeStampedAdmin, RelationshipDisplayMixin):
    """Admin for PortfolioItem model"""
    list_display = ("id", "title", "category", "client", "completionDate", "technologies_display")
    list_filter = ("category", "client", "completionDate", "technologies")
    search_fields = ("title", "description", "client")
    filter_horizontal = ("technologies",)
    date_hierarchy = "completionDate"
    
    def get_queryset(self, request):
        """Optimize queryset to prevent N+1 queries"""
        return super().get_queryset(request).prefetch_related('technologies')

    def technologies_display(self, obj):
        return self.render_related_list(obj, obj.technologies)
    technologies_display.short_description = "Technologies"


@admin.register(Service)
class ServiceAdmin(TranslationAdmin, TimeStampedAdmin, RelationshipDisplayMixin):
    """Admin for Service model"""
    list_display = ("id", "title", "pricing", "features_display")
    search_fields = ("id", "title", "description", "details")
    inlines = [ServiceFeatureInline]
    
    def get_queryset(self, request):
        """Optimize queryset to prevent N+1 queries"""
        return super().get_queryset(request).prefetch_related('service_features')

    def features_display(self, obj):
        return self.render_related_list(obj, obj.service_features)
    features_display.short_description = "Features"


@admin.register(TeamMember)
class TeamMemberAdmin(TranslationAdmin, OrderedAdmin, RelationshipDisplayMixin):
    """Admin for TeamMember model"""
    list_display = ("id", "name", "role", "order", "social_display")
    list_filter = ("role",)
    search_fields = ("name", "role", "bio")
    inlines = [SocialLinkInline]
    
    def get_queryset(self, request):
        """Optimize queryset to prevent N+1 queries"""
        return super().get_queryset(request).prefetch_related('social_links')

    def social_display(self, obj):
        return self.render_social_links(obj)
    social_display.short_description = "Social Links"


@admin.register(Testimonial)
class TestimonialAdmin(TranslationAdmin, OrderedAdmin):
    list_display = ("id", "name", "role", "order")
    list_filter = ("role",)
    search_fields = ("name", "role", "thoughts")


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ("id", "fullName", "email", "phone", "status", "createdAt")
    list_filter = ("status", "createdAt")
    search_fields = ("fullName", "email", "phone", "company", "subject")
    readonly_fields = ("createdAt",)
    date_hierarchy = "createdAt"
    ordering = ("-createdAt",)

from django import forms
from django.contrib import admin
from django.utils.html import format_html_join, format_html
from ckeditor.widgets import CKEditorWidget
from django import forms
from modeltranslation.admin import TranslationAdmin
from adminsortable2.admin import SortableAdminMixin, SortableInlineAdminMixin 
from .models import (
    BlogPost,
    PortfolioItem,
    PortfolioCategory,
    Service,
    TeamMember,
    Testimonial,
    ContactInquiry,
    Tag,
    Technology,
    ServiceFeature,
    SocialLink,
    Category,
    FAQ,
    HeaderNavLink
)


# --- Inline Admin Classes ---
class ServiceFeatureInline(SortableInlineAdminMixin, admin.TabularInline):  # ✅ sortable inline
    """Inline admin for service features"""
    model = ServiceFeature
    extra = 1
    ordering = ['order', 'id']

    def get_queryset(self, request):
        """Optimize inline queryset"""
        return super().get_queryset(request).select_related('service')


class SocialLinkInline(SortableInlineAdminMixin, admin.TabularInline):  # ✅ sortable inline
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


class OrderedAdmin(SortableAdminMixin, admin.ModelAdmin):  # ✅ make all ordered models sortable
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


# --- Admin Registrations ---
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)


@admin.register(Category)
class CategoryAdmin(OrderedAdmin):  # ✅ sortable
    list_display = ('name', 'order')
    search_fields = ('name',)


@admin.register(Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)


class BlogPostCategoryInline(admin.TabularInline):
    model = BlogPost.categories.through
    extra = 1

class BlogPostAdminForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = "__all__"
        widgets = {
            "content": CKEditorWidget(),     # Rich editor in Admin
        }

@admin.register(BlogPost)
class BlogPostAdmin(TranslationAdmin,OrderedAdmin, TimeStampedAdmin, RelationshipDisplayMixin):
    form = BlogPostAdminForm
    list_display = ("id", "title", "status", "date", "author", "tags_display", "categories_display")
    list_filter = ("status", "date", "author", "tags")
    search_fields = ("title", "excerpt", "content")
    autocomplete_fields = ("author",)
    filter_horizontal = ("tags", "categories")
    date_hierarchy = "date"
    inlines = [BlogPostCategoryInline]

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author').prefetch_related('tags', 'categories')

    def tags_display(self, obj):
        return self.render_related_list(obj, obj.tags)
    tags_display.short_description = "Tags"

    def categories_display(self, obj):
        return self.render_related_list(obj, obj.categories)
    categories_display.short_description = "Categories"


@admin.register(PortfolioCategory)
class PortfolioCategoryAdmin(OrderedAdmin):  # ✅ sortable
    list_display = ("id", "name", "slug", "order")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(PortfolioItem)
class PortfolioItemAdmin(OrderedAdmin,TranslationAdmin, TimeStampedAdmin, RelationshipDisplayMixin):
    list_display = ("id", "title", "categories_display", "client", "completionDate", "technologies_display")
    list_filter = ("categories", "client", "completionDate", "technologies")
    search_fields = ("title", "description", "client")
    filter_horizontal = ("technologies", "categories")
    date_hierarchy = "completionDate"

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("technologies", "categories")

    def technologies_display(self, obj):
        return self.render_related_list(obj, obj.technologies)
    technologies_display.short_description = "Technologies"

    def categories_display(self, obj):
        return self.render_related_list(obj, obj.categories)
    categories_display.short_description = "Categories"


@admin.register(Service)
class ServiceAdmin(OrderedAdmin,TranslationAdmin, TimeStampedAdmin, RelationshipDisplayMixin):
    list_display = ("id", "title", "pricing", "features_display")
    search_fields = ("id", "title", "description", "details")
    inlines = [ServiceFeatureInline]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('service_features')

    def features_display(self, obj):
        return self.render_related_list(obj, obj.service_features)
    features_display.short_description = "Features"


@admin.register(TeamMember)
class TeamMemberAdmin(TranslationAdmin, OrderedAdmin, RelationshipDisplayMixin):
    list_display = ("id", "name", "role", "order", "social_display")
    list_filter = ("role",)
    search_fields = ("name", "role", "bio")
    inlines = [SocialLinkInline]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('social_links')

    def social_display(self, obj):
        return self.render_social_links(obj)
    social_display.short_description = "Social Links"


@admin.register(Testimonial)
class TestimonialAdmin(TranslationAdmin, OrderedAdmin):  # ✅ sortable
    list_display = ("id", "name", "role", "order")
    list_filter = ("role",)
    search_fields = ("name", "role", "thoughts")


@admin.register(ContactInquiry)
class ContactInquiryAdmin(OrderedAdmin):
    list_display = ("id", "fullName", "email", "phone", "status", "createdAt")
    list_filter = ("status", "createdAt")
    search_fields = ("fullName", "email", "phone", "company", "subject")


@admin.register(FAQ)
class FAQAdmin(TranslationAdmin, OrderedAdmin):  # ✅ sortable
    list_display = ("id", "question", "is_active", "order", "createdAt")
    list_filter = ("is_active",)
    search_fields = ("question", "answer")
    list_editable = ("is_active", "order")


@admin.register(HeaderNavLink)
class HeaderNavLinkAdmin(TranslationAdmin, OrderedAdmin):  # ✅ sortable + nested
    list_display = (
        "id",
        "title",
        "parent_display",
        "url",
        "is_external",
        "is_active",
        "order",
        "createdAt",
    )
    list_filter = ("is_external", "is_active", "parent")
    search_fields = ("title", "url")
    list_editable = ("is_active", "order")
    autocomplete_fields = ("parent",)

    def parent_display(self, obj):
        return obj.parent.title if obj.parent else "-"
    parent_display.short_description = "Parent Link"

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("parent")

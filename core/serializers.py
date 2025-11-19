from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import (
    BlogPost, PortfolioItem, Service, TeamMember, Testimonial, ContactInquiry,
    Tag, Technology, ServiceFeature, SocialLink , Category  , HeaderNavLink , FAQ , PortfolioCategory
)

User = get_user_model()


# --- Serializers for New Models ---
class TagSerializer(serializers.ModelSerializer):
    """Serializer for Tag model"""
    class Meta:
        model = Tag
        fields = ('id', 'name', 'slug')


class TechnologySerializer(serializers.ModelSerializer):
    """Serializer for Technology model"""
    class Meta:
        model = Technology
        fields = ('id', 'name', 'slug')


class ServiceFeatureSerializer(serializers.ModelSerializer):
    """Serializer for ServiceFeature model"""
    class Meta:
        model = ServiceFeature
        fields = ('id', 'name', 'order')


class SocialLinkSerializer(serializers.ModelSerializer):
    """Serializer for SocialLink model"""
    platform_display = serializers.CharField(source='get_platform_display', read_only=True)
    
    class Meta:
        model = SocialLink
        fields = ('id', 'platform', 'platform_display', 'url', 'order')


# --- Main Model Serializers ---
class AuthorSerializer(serializers.ModelSerializer):
    """Serializer for User model as author"""
    class Meta:
        model = User
        fields = ("id", "username", "first_name", "last_name", "email")


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model"""
    class Meta:
        model = Category
        fields = ("id", "name", "order")

class BlogPostSerializer(serializers.ModelSerializer):
    """Serializer for BlogPost model with nested relationships"""
    author = AuthorSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    tags_list = serializers.SerializerMethodField(
        help_text="List of tag names for backward compatibility"
    )
    categories = CategorySerializer(many=True, read_only=True)
    categories_list = serializers.SerializerMethodField(
        help_text="List of category names for backward compatibility"
    )

    def get_tags_list(self, obj):
        """Get list of tag names for backward compatibility"""
        try:
            return obj.tags_list
        except AttributeError:
            return []
    def get_categories_list(self, obj):
        """Get list of category names for backward compatibility"""
        try:
            return obj.categories_list
        except AttributeError:
            return []

    class Meta:
        model = BlogPost
        fields = (
            "id", "title", "excerpt", "content", "date", "readTime",
            "image", "author", "tags", "tags_list", 'categories','categories_list',  "status", "createdAt", "updatedAt","order"
        )


class PortfolioCategorySerializer(serializers.ModelSerializer):
    """Serializer for PortfolioCategory model"""
    class Meta:
        model = PortfolioCategory
        fields = ("id", "name", "slug", "order")

class PortfolioItemSerializer(serializers.ModelSerializer):
    """Serializer for PortfolioItem model with nested relationships"""
    technologies = TechnologySerializer(many=True, read_only=True)
    categories = PortfolioCategorySerializer(many=True, read_only=True)

    technologies_list = serializers.SerializerMethodField(
        help_text="List of technology names for backward compatibility"
    )
    categories_list = serializers.SerializerMethodField(
        help_text="List of category names for backward compatibility"
    )

    class Meta:
        model = PortfolioItem
        fields = (
            "id", "title", "description", "image", "url", "categories",
            "technologies", "technologies_list", "categories_list",
            "client", "completionDate", "createdAt", "updatedAt","order"
        )

    def get_technologies_list(self, obj):
        """Get list of technology names for backward compatibility"""
        try:
            return obj.technologies_list
        except AttributeError:
            return []

    def get_categories_list(self, obj):
        """Get list of category names for backward compatibility"""
        try:
            return obj.categories_list
        except AttributeError:
            return []


class ServiceSerializer(serializers.ModelSerializer):
    """Serializer for Service model with nested relationships"""
    features = ServiceFeatureSerializer(source='service_features', many=True, read_only=True)
    features_list = serializers.SerializerMethodField(
        help_text="List of feature names for backward compatibility"
    )

    def get_features_list(self, obj):
        """Get list of feature names for backward compatibility"""
        try:
            return obj.features_list
        except AttributeError:
            return []

    class Meta:
        model = Service
        fields = (
            "id", "title", "description", "details", "image",
            "features", "features_list", "pricing", "createdAt", "updatedAt",
            "order",
        )


class TeamMemberSerializer(serializers.ModelSerializer):
    """Serializer for TeamMember model with nested relationships"""
    social_links = SocialLinkSerializer(many=True, read_only=True)
    social = serializers.SerializerMethodField(
        help_text="Social links as dictionary for backward compatibility"
    )

    def get_social(self, obj):
        """Get social links as dictionary for backward compatibility"""
        try:
            return obj.social_dict
        except AttributeError:
            return {}

    class Meta:
        model = TeamMember
        fields = (
            "id", "name", "role", "image", "bio", "social_links", "social", "order",
            "createdAt", "updatedAt","order"
        )


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = (
            "id", "name", "thoughts", "role", "instagramUrl", "order",
            "createdAt", "updatedAt","order"
        )


class ContactInquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInquiry
        fields = (
            "id", "fullName", "email", "phone", "company", "subject","order"
        )

class HeaderNavLinkSerializer(serializers.ModelSerializer):
    """Recursive serializer for Header Navigation Links"""
    children = serializers.SerializerMethodField()

    class Meta:
        model = HeaderNavLink
        fields = [
            "id",
            "title",
            "url",
            "is_external",
            "is_active",
            "order",
            "parent",
            "children",
            "order"
        ]

    def get_children(self, obj):
        """Recursively get active child links"""
        children_qs = obj.children.filter(is_active=True).order_by("order", "id")
        return HeaderNavLinkSerializer(children_qs, many=True, context=self.context).data

class FAQSerializer(serializers.ModelSerializer):
    """Serializer for FAQ model"""
    
    class Meta:
        model = FAQ
        fields = ["id", "question", "answer", "order", "is_active", "createdAt", "updatedAt","order"]
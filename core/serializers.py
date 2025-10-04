from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import (
    BlogPost, PortfolioItem, Service, TeamMember, Testimonial, ContactInquiry,
    Tag, Technology, ServiceFeature, SocialLink , Category  
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
            "image", "author", "tags", "tags_list", 'categories','categories_list',  "status", "createdAt", "updatedAt",
        )


class PortfolioItemSerializer(serializers.ModelSerializer):
    """Serializer for PortfolioItem model with nested relationships"""
    technologies = TechnologySerializer(many=True, read_only=True)
    technologies_list = serializers.SerializerMethodField(
        help_text="List of technology names for backward compatibility"
    )

    def get_technologies_list(self, obj):
        """Get list of technology names for backward compatibility"""
        try:
            return obj.technologies_list
        except AttributeError:
            return []

    class Meta:
        model = PortfolioItem
        fields = (
            "id", "title", "description", "image", "url", "category",
            "technologies", "technologies_list", "client", "completionDate", 
            "createdAt", "updatedAt",
        )


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
            "createdAt", "updatedAt",
        )


class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = (
            "id", "name", "thoughts", "role", "instagramUrl", "order",
            "createdAt", "updatedAt",
        )


class ContactInquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInquiry
        fields = (
            "id", "fullName", "email", "phone", "company", "subject",
            "status", 
        )

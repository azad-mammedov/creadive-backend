import logging
from django.db import transaction
from django.http import JsonResponse , HttpResponse

from django.db.models import Count, Q
from django.utils.translation import gettext_lazy as _ , get_language , activate
from django.core.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response 
from rest_framework.exceptions import NotFound, ValidationError as DRFValidationError

from .models import BlogPost, PortfolioItem, PortfolioCategory, Service, TeamMember, Testimonial, ContactInquiry , HeaderNavLink , FAQ
from .serializers import (
    BlogPostSerializer, PortfolioItemSerializer, ServiceSerializer,
    TeamMemberSerializer, TestimonialSerializer, ContactInquirySerializer , HeaderNavLinkSerializer , FAQSerializer , PortfolioCategorySerializer
)

logger = logging.getLogger(__name__)


class ErrorHandlingMixin:
    """Mixin to add consistent error handling to viewsets"""
    
    def handle_exception(self, exc):
        """Handle exceptions with logging and proper response format"""
        logger.error(f"Exception in {self.__class__.__name__}: {str(exc)}", exc_info=True)
        return super().handle_exception(exc)
    
    def safe_get_queryset(self):
        """Safely get queryset with error handling"""
        try:
            return self.get_queryset()
        except Exception as e:
            logger.error(f"Error getting queryset in {self.__class__.__name__}: {str(e)}")
            return self.queryset.none()
    
    def safe_filter_queryset(self, queryset):
        """Safely filter queryset with error handling"""
        try:
            return self.filter_queryset(queryset)
        except Exception as e:
            logger.error(f"Error filtering queryset in {self.__class__.__name__}: {str(e)}")
            return queryset.none()

# def debug_language(request):
#     # activate('ru')
#     session_lang = request.session.get('django_language')
#     cookie_lang = request.COOKIES.get('django_language')
#     accept_lang = request.META.get('HTTP_ACCEPT_LANGUAGE')
#     active_lang = get_language()
#     return HttpResponse(
#         f"Session: {session_lang}, Cookie: {cookie_lang}, Accept-Language: {accept_lang}, Active: {active_lang}"
#     )

class BlogPostViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for BlogPost model with optimized queries"""
    serializer_class = BlogPostSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["status", "categories", "tags"]
    search_fields = ["title", "excerpt", "content", "categories__name", "tags__name"]
    ordering_fields = ["date", "createdAt"]

    def get_queryset(self):
        
        return BlogPost.objects.select_related("author").prefetch_related("tags",'categories').all()


class PortfolioItemViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for PortfolioItem model with optimized queries"""
    queryset = PortfolioItem.objects.prefetch_related("technologies", "categories").all()
    serializer_class = PortfolioItemSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["client", "technologies", "categories"]
    search_fields = ["title", "description", "client", "technologies__name", "categories__name"]
    ordering_fields = ["completionDate", "createdAt"]

    @action(detail=False, methods=["get"], url_path="categories")
    def categories(self, request):
        """Return all portfolio categories with item counts"""
        data = (
            PortfolioCategory.objects.annotate(item_count=Count("portfolio_items"))
            .filter(item_count__gt=0)
            .order_by("order", "name")
        )
        serializer = PortfolioCategorySerializer(data, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path=r"category/(?P<slug>[^/]+)")
    def by_category(self, request, slug: str):
        """Return portfolio items filtered by category slug"""
        qs = self.get_queryset().filter(categories__slug=slug)
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Service model with optimized queries"""
    queryset = Service.objects.prefetch_related("service_features").all()
    serializer_class = ServiceSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["id", "title", "description", "details", "service_features__name"]
    ordering_fields = ["id", "createdAt"]


class TeamMemberViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for TeamMember model with optimized queries"""
    queryset = TeamMember.objects.prefetch_related("social_links").all()
    serializer_class = TeamMemberSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "role", "bio", "social_links__platform"]
    ordering_fields = ["order", "id"]


class TestimonialViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Testimonial model"""
    queryset = Testimonial.objects.all()
    serializer_class = TestimonialSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "role", "thoughts"]
    ordering_fields = ["order", "id"]


class ContactInquiryViewSet(viewsets.ModelViewSet):
    """ViewSet for ContactInquiry model with create endpoint"""
    queryset = ContactInquiry.objects.all()
    serializer_class = ContactInquirySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["fullName", "email", "phone", "company", "subject", "status"]
    ordering_fields = ["createdAt", "id"]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class FAQViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for FAQ model"""
    queryset = FAQ.objects.filter(is_active=True).order_by("order", "id")
    serializer_class = FAQSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["question", "answer"]
    ordering_fields = ["order", "id"]


class HeaderNavLinkViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for Header Navigation Links (supports nested dropdowns)"""
    queryset = (
        HeaderNavLink.objects.filter(is_active=True, parent__isnull=True)
        .prefetch_related("children")
        .order_by("order", "id")
    )
    serializer_class = HeaderNavLinkSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "url"]
    ordering_fields = ["order", "id"]
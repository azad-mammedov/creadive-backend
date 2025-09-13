import logging
from django.db import transaction
from django.db.models import Count, Q
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ValidationError as DRFValidationError

from .models import BlogPost, PortfolioItem, Service, TeamMember, Testimonial, ContactInquiry
from .serializers import (
    BlogPostSerializer, PortfolioItemSerializer, ServiceSerializer,
    TeamMemberSerializer, TestimonialSerializer, ContactInquirySerializer
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

class BlogPostViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for BlogPost model with optimized queries"""
    queryset = BlogPost.objects.select_related("author").prefetch_related("tags").all()
    serializer_class = BlogPostSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["status", "category", "tags"]
    search_fields = ["title", "excerpt", "content", "category", "tags__name"]
    ordering_fields = ["date", "createdAt"]


class PortfolioItemViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for PortfolioItem model with optimized queries"""
    queryset = PortfolioItem.objects.prefetch_related("technologies").all()
    serializer_class = PortfolioItemSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["category", "client", "technologies"]
    search_fields = ["title", "description", "client", "technologies__name"]
    ordering_fields = ["completionDate", "createdAt"]

    @action(detail=False, methods=["get"], url_path="categories")
    def categories(self, request):
        data = (
            PortfolioItem.objects.values("category")
            .exclude(category="")
            .annotate(count=Count("id"))
            .order_by("category")
        )
        return Response(list(data))

    @action(detail=False, methods=["get"], url_path=r"category/(?P<category>[^/]+)")
    def by_category(self, request, category: str):
        qs = self.get_queryset().filter(category=category)
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


class ContactInquiryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for ContactInquiry model"""
    queryset = ContactInquiry.objects.all()
    serializer_class = ContactInquirySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["fullName", "email", "phone", "company", "subject", "status"]
    ordering_fields = ["createdAt", "id"]

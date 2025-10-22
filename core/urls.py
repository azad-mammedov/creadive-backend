from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BlogPostViewSet, PortfolioItemViewSet, ServiceViewSet,
    TeamMemberViewSet, TestimonialViewSet, ContactInquiryViewSet , FAQViewSet , HeaderNavLinkViewSet
)
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

router = DefaultRouter()
router.register(r"blog", BlogPostViewSet, basename="blog")
router.register(r"portfolio", PortfolioItemViewSet, basename="portfolio")
router.register(r"services", ServiceViewSet, basename="services")
router.register(r"team", TeamMemberViewSet, basename="team")
router.register(r"testimonials", TestimonialViewSet, basename="testimonials")
router.register(r"contact", ContactInquiryViewSet, basename="contact")
router.register(r'faqs', FAQViewSet, basename='faq')
router.register(r'header-nav-links', HeaderNavLinkViewSet, basename='headernavlink')

urlpatterns = [
    path("", include(router.urls)),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),

    # Swagger UI
    path('docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # ReDoc UI
    path('docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc-ui'),
]

from modeltranslation.translator import translator, TranslationOptions
from .models import BlogPost, PortfolioItem, Service, TeamMember, Testimonial

class BlogPostTO(TranslationOptions):
    fields = ("title", "excerpt", "content", "category", "readTime")

class PortfolioItemTO(TranslationOptions):
    fields = ("title", "description", "category", "client")

class ServiceTO(TranslationOptions):
    fields = ("title", "description", "details")

class TeamMemberTO(TranslationOptions):
    fields = ("name", "role", "bio")

class TestimonialTO(TranslationOptions):
    fields = ("name", "thoughts", "role")

translator.register(BlogPost, BlogPostTO)
translator.register(PortfolioItem, PortfolioItemTO)
translator.register(Service, ServiceTO)
translator.register(TeamMember, TeamMemberTO)
translator.register(Testimonial, TestimonialTO)

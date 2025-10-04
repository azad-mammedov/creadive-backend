from modeltranslation.translator import translator, TranslationOptions
from .models import BlogPost, PortfolioItem, Service, TeamMember, Testimonial , Category

class BlogPostTO(TranslationOptions):
    fields = ("title", "excerpt", "content", "readTime")

class CategoryTO(TranslationOptions):
    fields = ("name",)
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
translator.register(Category, CategoryTO) 

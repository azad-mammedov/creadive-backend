from modeltranslation.translator import translator, TranslationOptions
from .models import BlogPost, PortfolioItem, PortfolioCategory ,Service, TeamMember, Testimonial , Category , FAQ , HeaderNavLink

class BlogPostTO(TranslationOptions):
    fields = ("title", "excerpt", "content", "readTime")

class CategoryTO(TranslationOptions):
    fields = ("name",)
class PortfolioItemTO(TranslationOptions):
    fields = ("title", "description", "client")

class PortfolioCategoryTO(TranslationOptions):
    fields = ("name",)

class ServiceTO(TranslationOptions):
    fields = ("title", "description", "details")

class TeamMemberTO(TranslationOptions):
    fields = ("name", "role", "bio")

class TestimonialTO(TranslationOptions):
    fields = ("name", "thoughts", "role")

class FAQTO(TranslationOptions):
    fields = ("question", "answer")

class HeaderNavLinkTO(TranslationOptions):
    fields = ("title",)

translator.register(BlogPost, BlogPostTO)
translator.register(PortfolioItem, PortfolioItemTO)
translator.register(PortfolioCategory, PortfolioCategoryTO)
translator.register(Service, ServiceTO)
translator.register(TeamMember, TeamMemberTO)
translator.register(Testimonial, TestimonialTO)
translator.register(Category, CategoryTO) 
translator.register(FAQ, FAQTO)
translator.register(HeaderNavLink, HeaderNavLinkTO)
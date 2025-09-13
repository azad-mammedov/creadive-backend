import json
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone, translation
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from datetime import date, datetime

from .models import (
    BlogPost, PortfolioItem, Service, TeamMember, Testimonial, ContactInquiry,
    Tag, Technology, ServiceFeature, SocialLink
)

User = get_user_model()


class BaseTestSetup:
    """Base setup for creating test data"""
    
    @classmethod
    def create_user(cls, **kwargs):
        """Create a test user"""
        defaults = {
            'username': 'testuser',
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
        defaults.update(kwargs)
        return User.objects.create_user(**defaults)
    
    @classmethod
    def create_tag(cls, **kwargs):
        """Create a test tag"""
        defaults = {
            'name': 'Test Tag',
            'slug': 'test-tag'
        }
        defaults.update(kwargs)
        return Tag.objects.create(**defaults)
    
    @classmethod
    def create_technology(cls, **kwargs):
        """Create a test technology"""
        defaults = {
            'name': 'Test Tech',
            'slug': 'test-tech'
        }
        defaults.update(kwargs)
        return Technology.objects.create(**defaults)
    
    @classmethod
    def create_blog_post(cls, user=None, tags=None, **kwargs):
        """Create a test blog post"""
        if user is None:
            user = cls.create_user()
        
        defaults = {
            'title': 'Test Blog Post',
            'excerpt': 'Test excerpt',
            'content': 'Test content',
            'category': 'Test Category',
            'date': date.today(),
            'readTime': '5 min',
            'image': 'https://example.com/image.jpg',
            'author': user,
            'status': 'published'
        }
        defaults.update(kwargs)
        
        blog_post = BlogPost.objects.create(**defaults)
        
        if tags:
            blog_post.tags.set(tags)
        
        return blog_post
    
    @classmethod
    def create_portfolio_item(cls, technologies=None, **kwargs):
        """Create a test portfolio item"""
        defaults = {
            'title': 'Test Portfolio Item',
            'description': 'Test description',
            'image': 'https://example.com/portfolio.jpg',
            'url': 'https://example.com/project',
            'category': 'Web Development',
            'client': 'Test Client',
            'completionDate': date.today()
        }
        defaults.update(kwargs)
        
        portfolio_item = PortfolioItem.objects.create(**defaults)
        
        if technologies:
            portfolio_item.technologies.set(technologies)
        
        return portfolio_item
    
    @classmethod
    def create_service(cls, **kwargs):
        """Create a test service"""
        defaults = {
            'id': 'test-service',
            'title': 'Test Service',
            'description': 'Test description',
            'details': 'Test details',
            'image': 'https://example.com/service.jpg',
            'pricing': '$100'
        }
        defaults.update(kwargs)
        return Service.objects.create(**defaults)
    
    @classmethod
    def create_team_member(cls, **kwargs):
        """Create a test team member"""
        defaults = {
            'name': 'Test Member',
            'role': 'Developer',
            'image': 'https://example.com/member.jpg',
            'bio': 'Test bio',
            'order': 1
        }
        defaults.update(kwargs)
        return TeamMember.objects.create(**defaults)
    
    @classmethod
    def create_testimonial(cls, **kwargs):
        """Create a test testimonial"""
        defaults = {
            'name': 'Test Client',
            'thoughts': 'Great work!',
            'role': 'CEO',
            'instagramUrl': 'https://instagram.com/test',
            'order': 1
        }
        defaults.update(kwargs)
        return Testimonial.objects.create(**defaults)
    
    @classmethod
    def create_contact_inquiry(cls, **kwargs):
        """Create a test contact inquiry"""
        defaults = {
            'fullName': 'John Doe',
            'email': 'john@example.com',
            'phone': '+1234567890',
            'company': 'Test Company',
            'subject': 'Test inquiry',
            'status': 'new'
        }
        defaults.update(kwargs)
        return ContactInquiry.objects.create(**defaults)


# =============================================================================
# MODEL TESTS
# =============================================================================

class ModelTests(TestCase, BaseTestSetup):
    """Test cases for model functionality"""
    
    def test_tag_creation(self):
        """Test tag model creation"""
        tag = self.create_tag()
        self.assertEqual(str(tag), 'Test Tag')
        self.assertEqual(tag.slug, 'test-tag')
    
    def test_technology_creation(self):
        """Test technology model creation"""
        tech = self.create_technology()
        self.assertEqual(str(tech), 'Test Tech')
        self.assertEqual(tech.slug, 'test-tech')
    
    def test_blog_post_creation(self):
        """Test blog post model creation and relationships"""
        user = self.create_user()
        tag1 = self.create_tag(name='Tag 1', slug='tag-1')
        tag2 = self.create_tag(name='Tag 2', slug='tag-2')
        
        blog_post = self.create_blog_post(user=user, tags=[tag1, tag2])
        
        self.assertEqual(str(blog_post), 'Test Blog Post')
        self.assertEqual(blog_post.author, user)
        self.assertEqual(blog_post.tags.count(), 2)
        self.assertIn(tag1, blog_post.tags.all())
        self.assertIn(tag2, blog_post.tags.all())
        
        # Test tags_list property
        tag_names = blog_post.tags_list
        self.assertIn('Tag 1', tag_names)
        self.assertIn('Tag 2', tag_names)
    
    def test_portfolio_item_creation(self):
        """Test portfolio item model creation and relationships"""
        tech1 = self.create_technology(name='React', slug='react')
        tech2 = self.create_technology(name='Django', slug='django')
        
        portfolio_item = self.create_portfolio_item(technologies=[tech1, tech2])
        
        self.assertEqual(str(portfolio_item), 'Test Portfolio Item')
        self.assertEqual(portfolio_item.technologies.count(), 2)
        self.assertIn(tech1, portfolio_item.technologies.all())
        self.assertIn(tech2, portfolio_item.technologies.all())
        
        # Test technologies_list property
        tech_names = portfolio_item.technologies_list
        self.assertIn('React', tech_names)
        self.assertIn('Django', tech_names)
    
    def test_service_creation_with_features(self):
        """Test service model creation with features"""
        service = self.create_service()
        
        # Add features
        feature1 = ServiceFeature.objects.create(
            service=service, name='Feature 1', order=1
        )
        feature2 = ServiceFeature.objects.create(
            service=service, name='Feature 2', order=2
        )
        
        self.assertEqual(str(service), 'Test Service')
        self.assertEqual(service.service_features.count(), 2)
        
        # Test features_list property
        feature_names = service.features_list
        self.assertIn('Feature 1', feature_names)
        self.assertIn('Feature 2', feature_names)
    
    def test_team_member_with_social_links(self):
        """Test team member model with social links"""
        team_member = self.create_team_member()
        
        # Add social links
        social1 = SocialLink.objects.create(
            team_member=team_member,
            platform='twitter',
            url='https://twitter.com/test',
            order=1
        )
        social2 = SocialLink.objects.create(
            team_member=team_member,
            platform='linkedin',
            url='https://linkedin.com/in/test',
            order=2
        )
        
        self.assertEqual(str(team_member), 'Test Member')
        self.assertEqual(team_member.social_links.count(), 2)
        
        # Test social_dict property
        social_dict = team_member.social_dict
        self.assertEqual(social_dict['twitter'], 'https://twitter.com/test')
        self.assertEqual(social_dict['linkedin'], 'https://linkedin.com/in/test')
    
    def test_testimonial_creation(self):
        """Test testimonial model creation"""
        testimonial = self.create_testimonial()
        self.assertEqual(str(testimonial), 'Test Client')
    
    def test_contact_inquiry_creation(self):
        """Test contact inquiry model creation"""
        inquiry = self.create_contact_inquiry()
        self.assertIn('John Doe', str(inquiry))
        self.assertIn('Test inquiry', str(inquiry))


# =============================================================================
# API ENDPOINT TESTS
# =============================================================================

class BlogPostAPITests(APITestCase, BaseTestSetup):
    """Test cases for BlogPost API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = self.create_user()
        self.tag1 = self.create_tag(name='Django', slug='django')
        self.tag2 = self.create_tag(name='Python', slug='python')
        
        self.published_post = self.create_blog_post(
            user=self.user,
            tags=[self.tag1, self.tag2],
            title='Published Post',
            status='published'
        )
        
        self.draft_post = self.create_blog_post(
            user=self.user,
            title='Draft Post',
            status='draft'
        )
    
    def test_list_blog_posts(self):
        """Test listing blog posts"""
        url = reverse('blog-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)  # Only published posts
        self.assertEqual(response.data['results'][0]['title'], 'Published Post')
    
    def test_retrieve_blog_post(self):
        """Test retrieving a single blog post"""
        url = reverse('blog-detail', kwargs={'pk': self.published_post.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Published Post')
        self.assertEqual(len(response.data['tags']), 2)
        self.assertIn('Django', response.data['tags_list'])
        self.assertIn('Python', response.data['tags_list'])
    
    def test_filter_blog_posts_by_status(self):
        """Test filtering blog posts by status"""
        url = reverse('blog-list')
        response = self.client.get(url, {'status': 'published'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_filter_blog_posts_by_category(self):
        """Test filtering blog posts by category"""
        url = reverse('blog-list')
        response = self.client.get(url, {'category': 'Test Category'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_search_blog_posts(self):
        """Test searching blog posts"""
        url = reverse('blog-list')
        response = self.client.get(url, {'search': 'Published'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Published Post')
    
    def test_order_blog_posts(self):
        """Test ordering blog posts"""
        # Create another post with a different date
        old_post = self.create_blog_post(
            user=self.user,
            title='Old Post',
            date=date(2020, 1, 1),
            status='published'
        )
        
        url = reverse('blog-list')
        response = self.client.get(url, {'ordering': 'date'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'][0]['title'], 'Old Post')
        
        # Test reverse ordering
        response = self.client.get(url, {'ordering': '-date'})
        self.assertEqual(response.data['results'][0]['title'], 'Published Post')
    
    def test_blog_post_categories_endpoint(self):
        """Test the categories endpoint"""
        # Create posts with different categories
        self.create_blog_post(
            user=self.user,
            category='Tech',
            status='published'
        )
        self.create_blog_post(
            user=self.user,
            category='Tech',
            status='published'
        )
        
        url = reverse('blog-categories')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        categories = [item['category'] for item in response.data]
        self.assertIn('Tech', categories)
        self.assertIn('Test Category', categories)
    
    def test_blog_post_by_category_endpoint(self):
        """Test the by_category endpoint"""
        self.create_blog_post(
            user=self.user,
            category='Tech',
            title='Tech Post',
            status='published'
        )
        
        url = reverse('blog-by-category', kwargs={'category': 'Tech'})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Tech Post')


class PortfolioItemAPITests(APITestCase, BaseTestSetup):
    """Test cases for PortfolioItem API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.tech1 = self.create_technology(name='React', slug='react')
        self.tech2 = self.create_technology(name='Django', slug='django')
        
        self.portfolio_item = self.create_portfolio_item(
            technologies=[self.tech1, self.tech2],
            category='Web Development'
        )
    
    def test_list_portfolio_items(self):
        """Test listing portfolio items"""
        url = reverse('portfolio-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Test Portfolio Item')
    
    def test_retrieve_portfolio_item(self):
        """Test retrieving a single portfolio item"""
        url = reverse('portfolio-detail', kwargs={'pk': self.portfolio_item.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Portfolio Item')
        self.assertEqual(len(response.data['technologies']), 2)
        self.assertIn('React', response.data['technologies_list'])
        self.assertIn('Django', response.data['technologies_list'])
    
    def test_filter_portfolio_by_category(self):
        """Test filtering portfolio items by category"""
        url = reverse('portfolio-list')
        response = self.client.get(url, {'category': 'Web Development'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_portfolio_categories_endpoint(self):
        """Test the portfolio categories endpoint"""
        url = reverse('portfolio-categories')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        categories = [item['category'] for item in response.data]
        self.assertIn('Web Development', categories)
    
    def test_portfolio_by_category_endpoint(self):
        """Test the portfolio by_category endpoint"""
        url = reverse('portfolio-by-category', kwargs={'category': 'Web Development'})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['category'], 'Web Development')


class ServiceAPITests(APITestCase, BaseTestSetup):
    """Test cases for Service API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.service = self.create_service()
        
        # Add features
        ServiceFeature.objects.create(
            service=self.service,
            name='Feature 1',
            order=1
        )
        ServiceFeature.objects.create(
            service=self.service,
            name='Feature 2',
            order=2
        )
    
    def test_list_services(self):
        """Test listing services"""
        url = reverse('services-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], 'Test Service')
    
    def test_retrieve_service(self):
        """Test retrieving a single service"""
        url = reverse('services-detail', kwargs={'pk': self.service.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Service')
        self.assertEqual(len(response.data['features']), 2)
        self.assertIn('Feature 1', response.data['features_list'])
        self.assertIn('Feature 2', response.data['features_list'])
    
    def test_search_services(self):
        """Test searching services"""
        url = reverse('services-list')
        response = self.client.get(url, {'search': 'Test Service'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)


class TeamMemberAPITests(APITestCase, BaseTestSetup):
    """Test cases for TeamMember API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.team_member = self.create_team_member()
        
        # Add social links
        SocialLink.objects.create(
            team_member=self.team_member,
            platform='twitter',
            url='https://twitter.com/test',
            order=1
        )
        SocialLink.objects.create(
            team_member=self.team_member,
            platform='linkedin',
            url='https://linkedin.com/in/test',
            order=2
        )
    
    def test_list_team_members(self):
        """Test listing team members"""
        url = reverse('team-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Test Member')
    
    def test_retrieve_team_member(self):
        """Test retrieving a single team member"""
        url = reverse('team-detail', kwargs={'pk': self.team_member.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Member')
        self.assertEqual(len(response.data['social_links']), 2)
        self.assertEqual(response.data['social']['twitter'], 'https://twitter.com/test')
        self.assertEqual(response.data['social']['linkedin'], 'https://linkedin.com/in/test')


class TestimonialAPITests(APITestCase, BaseTestSetup):
    """Test cases for Testimonial API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.testimonial = self.create_testimonial()
    
    def test_list_testimonials(self):
        """Test listing testimonials"""
        url = reverse('testimonials-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['name'], 'Test Client')
    
    def test_retrieve_testimonial(self):
        """Test retrieving a single testimonial"""
        url = reverse('testimonials-detail', kwargs={'pk': self.testimonial.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Client')
        self.assertEqual(response.data['thoughts'], 'Great work!')


class ContactInquiryAPITests(APITestCase, BaseTestSetup):
    """Test cases for ContactInquiry API endpoints"""
    
    def setUp(self):
        self.client = APIClient()
        self.inquiry = self.create_contact_inquiry()
    
    def test_list_contact_inquiries(self):
        """Test listing contact inquiries"""
        url = reverse('contact-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['fullName'], 'John Doe')
    
    def test_retrieve_contact_inquiry(self):
        """Test retrieving a single contact inquiry"""
        url = reverse('contact-detail', kwargs={'pk': self.inquiry.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['fullName'], 'John Doe')
        self.assertEqual(response.data['subject'], 'Test inquiry')


# =============================================================================
# TRANSLATION TESTS
# =============================================================================

class TranslationTests(APITestCase, BaseTestSetup):
    """Test cases for model translations"""
    
    def setUp(self):
        self.client = APIClient()
        self.user = self.create_user()
    
    def test_blog_post_translations(self):
        """Test blog post translations"""
        # Create blog post with English content
        blog_post = self.create_blog_post(
            user=self.user,
            title='English Title',
            excerpt='English excerpt',
            content='English content',
            category='English Category'
        )
        
        # Add Spanish translations
        blog_post.title_es = 'Título Español'
        blog_post.excerpt_es = 'Extracto español'
        blog_post.content_es = 'Contenido español'
        blog_post.category_es = 'Categoría Española'
        blog_post.save()
        
        # Add French translations
        blog_post.title_fr = 'Titre Français'
        blog_post.excerpt_fr = 'Extrait français'
        blog_post.content_fr = 'Contenu français'
        blog_post.category_fr = 'Catégorie Française'
        blog_post.save()
        
        # Test English (default)
        url = reverse('blog-detail', kwargs={'pk': blog_post.pk})
        response = self.client.get(url, HTTP_ACCEPT_LANGUAGE='en')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'English Title')
        self.assertEqual(response.data['excerpt'], 'English excerpt')
        self.assertEqual(response.data['content'], 'English content')
        self.assertEqual(response.data['category'], 'English Category')
        
        # Test Spanish
        with translation.override('es'):
            response = self.client.get(url, HTTP_ACCEPT_LANGUAGE='es')
            
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['title'], 'Título Español')
            self.assertEqual(response.data['excerpt'], 'Extracto español')
            self.assertEqual(response.data['content'], 'Contenido español')
            self.assertEqual(response.data['category'], 'Categoría Española')
        
        # Test French
        with translation.override('fr'):
            response = self.client.get(url, HTTP_ACCEPT_LANGUAGE='fr')
            
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['title'], 'Titre Français')
            self.assertEqual(response.data['excerpt'], 'Extrait français')
            self.assertEqual(response.data['content'], 'Contenu français')
            self.assertEqual(response.data['category'], 'Catégorie Française')
    
    def test_portfolio_item_translations(self):
        """Test portfolio item translations"""
        portfolio_item = self.create_portfolio_item(
            title='English Portfolio',
            description='English description',
            category='English Category',
            client='English Client'
        )
        
        # Add Spanish translations
        portfolio_item.title_es = 'Portfolio Español'
        portfolio_item.description_es = 'Descripción española'
        portfolio_item.category_es = 'Categoría Española'
        portfolio_item.client_es = 'Cliente Español'
        portfolio_item.save()
        
        # Test English
        url = reverse('portfolio-detail', kwargs={'pk': portfolio_item.pk})
        response = self.client.get(url, HTTP_ACCEPT_LANGUAGE='en')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'English Portfolio')
        self.assertEqual(response.data['description'], 'English description')
        
        # Test Spanish
        with translation.override('es'):
            response = self.client.get(url, HTTP_ACCEPT_LANGUAGE='es')
            
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['title'], 'Portfolio Español')
            self.assertEqual(response.data['description'], 'Descripción española')
    
    def test_service_translations(self):
        """Test service translations"""
        service = self.create_service(
            title='English Service',
            description='English description',
            details='English details'
        )
        
        # Add Spanish translations
        service.title_es = 'Servicio Español'
        service.description_es = 'Descripción española'
        service.details_es = 'Detalles españoles'
        service.save()
        
        # Test English
        url = reverse('services-detail', kwargs={'pk': service.pk})
        response = self.client.get(url, HTTP_ACCEPT_LANGUAGE='en')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'English Service')
        self.assertEqual(response.data['description'], 'English description')
        self.assertEqual(response.data['details'], 'English details')
        
        # Test Spanish
        with translation.override('es'):
            response = self.client.get(url, HTTP_ACCEPT_LANGUAGE='es')
            
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['title'], 'Servicio Español')
            self.assertEqual(response.data['description'], 'Descripción española')
            self.assertEqual(response.data['details'], 'Detalles españoles')
    
    def test_team_member_translations(self):
        """Test team member translations"""
        team_member = self.create_team_member(
            name='English Name',
            role='English Role',
            bio='English bio'
        )
        
        # Add Spanish translations
        team_member.name_es = 'Nombre Español'
        team_member.role_es = 'Rol Español'
        team_member.bio_es = 'Biografía española'
        team_member.save()
        
        # Test English
        url = reverse('team-detail', kwargs={'pk': team_member.pk})
        response = self.client.get(url, HTTP_ACCEPT_LANGUAGE='en')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'English Name')
        self.assertEqual(response.data['role'], 'English Role')
        self.assertEqual(response.data['bio'], 'English bio')
        
        # Test Spanish
        with translation.override('es'):
            response = self.client.get(url, HTTP_ACCEPT_LANGUAGE='es')
            
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['name'], 'Nombre Español')
            self.assertEqual(response.data['role'], 'Rol Español')
            self.assertEqual(response.data['bio'], 'Biografía española')
    
    def test_testimonial_translations(self):
        """Test testimonial translations"""
        testimonial = self.create_testimonial(
            name='English Name',
            thoughts='English thoughts',
            role='English Role'
        )
        
        # Add Spanish translations
        testimonial.name_es = 'Nombre Español'
        testimonial.thoughts_es = 'Pensamientos españoles'
        testimonial.role_es = 'Rol Español'
        testimonial.save()
        
        # Test English
        url = reverse('testimonials-detail', kwargs={'pk': testimonial.pk})
        response = self.client.get(url, HTTP_ACCEPT_LANGUAGE='en')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'English Name')
        self.assertEqual(response.data['thoughts'], 'English thoughts')
        self.assertEqual(response.data['role'], 'English Role')
        
        # Test Spanish
        with translation.override('es'):
            response = self.client.get(url, HTTP_ACCEPT_LANGUAGE='es')
            
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['name'], 'Nombre Español')
            self.assertEqual(response.data['thoughts'], 'Pensamientos españoles')
            self.assertEqual(response.data['role'], 'Rol Español')
    
    def test_translation_fallback(self):
        """Test translation fallback behavior"""
        blog_post = self.create_blog_post(
            user=self.user,
            title='English Title'
        )
        
        # Only add Spanish translation for title, not for other fields
        blog_post.title_es = 'Título Español'
        blog_post.save()
        
        # Test Spanish - should get Spanish title but English content
        with translation.override('es'):
            url = reverse('blog-detail', kwargs={'pk': blog_post.pk})
            response = self.client.get(url, HTTP_ACCEPT_LANGUAGE='es')
            
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['title'], 'Título Español')
            # Should fallback to English for non-translated fields
            self.assertEqual(response.data['excerpt'], 'Test excerpt')
            self.assertEqual(response.data['content'], 'Test content')
    
    def test_list_translations(self):
        """Test translations in list endpoints"""
        blog_post1 = self.create_blog_post(
            user=self.user,
            title='English Post 1',
            status='published'
        )
        blog_post2 = self.create_blog_post(
            user=self.user,
            title='English Post 2',
            status='published'
        )
        
        # Add Spanish translations
        blog_post1.title_es = 'Post Español 1'
        blog_post1.save()
        
        blog_post2.title_es = 'Post Español 2'
        blog_post2.save()
        
        # Test list in Spanish
        with translation.override('es'):
            url = reverse('blog-list')
            response = self.client.get(url, HTTP_ACCEPT_LANGUAGE='es')
            
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            titles = [post['title'] for post in response.data['results']]
            self.assertIn('Post Español 1', titles)
            self.assertIn('Post Español 2', titles)
    
    def test_search_in_translated_fields(self):
        """Test searching in translated fields"""
        blog_post = self.create_blog_post(
            user=self.user,
            title='English Technology Post',
            content='This is about Django framework',
            status='published'
        )
        
        # Add Spanish translation
        blog_post.title_es = 'Post Español de Tecnología'
        blog_post.content_es = 'Esto es sobre el framework Django'
        blog_post.save()
        
        # Test search in English
        url = reverse('blog-list')
        response = self.client.get(url, {'search': 'Technology'}, HTTP_ACCEPT_LANGUAGE='en')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        
        # Test search in Spanish
        with translation.override('es'):
            response = self.client.get(url, {'search': 'Tecnología'}, HTTP_ACCEPT_LANGUAGE='es')
            
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data['results']), 1)

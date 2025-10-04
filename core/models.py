from django.conf import settings
from django.db import models
from django.utils import timezone
import uuid, os


class TimeStampedModel(models.Model):
    createdAt = models.DateTimeField(default=timezone.now, editable=False)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Tag(models.Model):
    """Model to represent tags for blog posts"""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Technology(models.Model):
    """Model to represent technologies for portfolio items"""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Technologies'
    
    def __str__(self):
        return self.name


class ServiceFeature(models.Model):
    """Model to represent features for services"""
    service = models.ForeignKey('Service', on_delete=models.CASCADE, related_name='service_features')
    name = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'id']
        unique_together = ['service', 'name']
    
    def __str__(self):
        return f"{self.service.title} - {self.name}"


class SocialLink(models.Model):
    """Model to represent social media links for team members"""
    PLATFORM_CHOICES = [
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter'),
        ('instagram', 'Instagram'),
        ('linkedin', 'LinkedIn'),
        ('github', 'GitHub'),
        ('youtube', 'YouTube'),
        ('website', 'Website'),
        ('other', 'Other'),
    ]
    
    team_member = models.ForeignKey('TeamMember', on_delete=models.CASCADE, related_name='social_links')
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    url = models.URLField(max_length=500)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'id']
        unique_together = ['team_member', 'platform']
    
    def __str__(self):
        return f"{self.team_member.name} - {self.get_platform_display()}"




class Category(models.Model):
    """Blog category model"""
    name = models.CharField(max_length=100, unique=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.name

def blog_image_upload_to(instance, filename):
        ext = os.path.splitext(filename)[1]
        unique_name = f"{uuid.uuid4().hex}{ext}"
        return f"blog_images/{unique_name}"

class BlogPost(TimeStampedModel):
    """Blog post model with proper relationships"""
    STATUS_CHOICES = [("published", "Published"), ("draft", "Draft")]
    
    title = models.CharField(max_length=255)
    excerpt = models.TextField(blank=True)
    content = models.TextField()
    date = models.DateField()
    readTime = models.CharField(max_length=50, blank=True)
    

    image = models.ImageField(upload_to=blog_image_upload_to, blank=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL, 
        related_name="posts"
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name="blog_posts")
    categories = models.ManyToManyField(
        Category, blank=True, related_name="blog_posts"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")

    class Meta:
        ordering = ["-date", "-id"]

    def __str__(self):
        return self.title
    
    @property
    def tags_list(self):
        """Return list of tag names for backward compatibility"""
        return list(self.tags.values_list('name', flat=True))
    
    @property
    def categories_list(self):
        """Return list of category names for backward compatibility"""
        return list(self.categories.values_list('name', flat=True))


def portfolio_image_upload_to(instance, filename):
        ext = os.path.splitext(filename)[1]
        unique_name = f"{uuid.uuid4().hex}{ext}"
        return f"portfolio_images/{unique_name}"

class PortfolioItem(TimeStampedModel):
    """Portfolio item model with proper relationships"""
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)


    image = models.ImageField(upload_to=portfolio_image_upload_to, blank=True)
    url = models.URLField(max_length=500, blank=True)
    category = models.CharField(max_length=100, blank=True)
    technologies = models.ManyToManyField(Technology, blank=True, related_name="portfolio_items")
    client = models.CharField(max_length=255, blank=True)
    completionDate = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["-completionDate", "id"]

    def __str__(self):
        return self.title
    
    @property
    def technologies_list(self):
        """Return list of technology names for backward compatibility"""
        return list(self.technologies.values_list('name', flat=True))


def service_image_upload_to(instance, filename):
        ext = os.path.splitext(filename)[1]
        unique_name = f"{uuid.uuid4().hex}{ext}"
        return f"service_images/{unique_name}"

class Service(TimeStampedModel):
    """Service model with related features"""
    id = models.CharField(primary_key=True, max_length=100)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    details = models.TextField(blank=True)
    image = models.ImageField(upload_to=service_image_upload_to, blank=True)
    pricing = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.title
    
    @property
    def features_list(self):
        """Return list of feature names for backward compatibility"""
        return list(self.service_features.values_list('name', flat=True))

def team_member_image_upload_to(instance, filename):
    ext = os.path.splitext(filename)[1]
    unique_name = f"{uuid.uuid4().hex}{ext}"
    return f"team_member_images/{unique_name}"


class TeamMember(TimeStampedModel):
    """Team member model with related social links"""
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to=team_member_image_upload_to, blank=True)
    bio = models.TextField(blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.name
    
    @property
    def social_dict(self):
        """Return social links as dictionary for backward compatibility"""
        return {link.platform: link.url for link in self.social_links.all()}


class Testimonial(TimeStampedModel):
    name = models.CharField(max_length=255)
    thoughts = models.TextField()
    role = models.CharField(max_length=255, blank=True)
    instagramUrl = models.URLField(max_length=500, blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.name


class ContactInquiry(models.Model):
    STATUS_CHOICES = [("new", "New"), ("handled", "Handled")]
    fullName = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    phone = models.CharField(max_length=100)
    company = models.CharField(max_length=255, blank=True)
    subject = models.TextField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="new")
    createdAt = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        ordering = ["-createdAt", "-id"]

    def __str__(self):
        return f"{self.fullName} - {self.subject[:30]}"

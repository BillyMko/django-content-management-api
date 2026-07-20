from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify


class User(AbstractUser):
    ROLE_CHOICES = [("student","Student"),
                    ("instructor", "Instructor"),
                    ("admin", "Admin")]
    
    STATUS = [("pending", "Pending"),
              ("approved", "Approved"),
              ("rejected", "Rejected"),
              ("suspended","Suspended")]
    
    status = models.CharField(max_length=20, choices = STATUS, default ="approved")
    
    role = models.CharField(max_length=20, choices = ROLE_CHOICES, default = "student")



class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True,blank=True)
    description = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug

            counter = 1
            while Category.objects.filter(slug = slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter = counter + 1

            self.slug = slug
        else:
            base_slug = slugify(self.slug)
            slug = base_slug

            counter = 1
            while Category.objects.filter(slug = slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter = counter + 1

            self.slug = slug
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Tag.objects.filter(slug = slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter = counter + 1

            self.slug = slug
        else:
            base_slug = slugify(self.slug)
            slug = base_slug

            counter = 1
            while Tag.objects.filter(slug = slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter = counter + 1

            self.slug = slug
        
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Content(models.Model):

    DIFFICULTY_CHOICES = [('beginner', 'Beginner'),
                        ('intermediate', 'Intermediate'),
                        ('advanced', 'Advanced'), 
                        ('expert', 'Expert')]
    title = models.CharField(max_length=200)
    body = models.TextField()
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    difficulty = models.CharField(max_length = 20, choices = DIFFICULTY_CHOICES, default='beginner')
    metadata = models.JSONField(default=dict, blank=True)

    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="contents")
    tags = models.ManyToManyField(Tag, blank=True, related_name="contents")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="contents")
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while Content.objects.filter(slug = slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter = counter + 1

            self.slug = slug
        else:
            base_slug = slugify(self.slug)
            slug = base_slug

            counter = 1
            while Content.objects.filter(slug = slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter = counter + 1

            self.slug = slug
        return super().save(*args, **kwargs)

class ContentView(models.Model):
    viewed_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="content_views")
    content= models.ForeignKey(Content, on_delete=models.CASCADE, related_name="views")

    def __str__(self):
        return f"{self.content.title} viewed at {self.viewed_at}"



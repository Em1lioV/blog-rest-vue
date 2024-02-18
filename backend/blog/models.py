from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from autoslug import AutoSlugField

class Role(models.Model):
    description =models.CharField(max_length=255)

    def __str__(self):
        return self.description


class User(AbstractUser):
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    initials = models.CharField(max_length=4)
    password = models.CharField(max_length=255)
    username = None
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='user_role', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstName', 'lastName', 'initials']
    
    def __str__(self):
        return self.email
    
    @property
    def fullname(self):
        return f"{self.firstName} {self.lastName}"
    


def user_directory_path(instance,filename):
    return 'blog/{0}/{1}'.format(instance.slug,filename)

class Post(models.Model):
    class PostObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='published')
    options = (
        ('draft','Draft'),
        ('published', 'Published')
    )
    title = models.CharField(max_length=250)
    thumbnail = models.ImageField(upload_to=user_directory_path,blank=True, null=True)
    excerpt =models.TextField(null=True)
    content = models.TextField()
    slug = AutoSlugField(populate_from='title', unique=True)
    published = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name='post_user')
    status = models.CharField(max_length=10,choices=options, default='draft')
    objects = models.Manager()
    postobjects = PostObjects()
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('-published',)

    def __str__(self):
        return self.title
    
    




from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class Role(models.Model):
    description =models.CharField(max_length=255)

    def __str__(self):
        return self.description


class User(AbstractUser):
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='user_role')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.email

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
    slug = models.SlugField(max_length=250, unique_for_date='published',null=False,unique=True)
    published = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE,related_name='post_user')
    status = models.CharField(max_length=10,choices=options, default='draft')
    objects = models.Manager()
    postobjects = PostObjects()

    class Meta:
        ordering = ('-published',)

    def __str__(self):
        return self.title
    
    




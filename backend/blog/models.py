from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from autoslug import AutoSlugField

class Role(models.Model):
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = AutoSlugField(populate_from='name', unique=True)

    def __str__(self):
        return self.name

    @property
    def follower_count(self):
        return self.followers.count()

    @property
    def post_count(self):
        return self.posts.count()

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Tags'
    
class User(AbstractUser):
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    initials = models.CharField(max_length=4)
    password = models.CharField(max_length=255)
    username = None
    presentation  = models.TextField(blank=True, null=True)
    biography  = models.CharField(max_length=255, blank=True, null=True)
    
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='user_role', blank=True, null=True)
    
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)
    followed_tags = models.ManyToManyField(Tag, related_name='followers', blank=True)
    
    bookmarks = models.ManyToManyField('Post', related_name='bookmarked_by', blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['firstName', 'lastName', 'initials']
    
    def __str__(self):
        return self.email
    
    @property
    def fullname(self):
        return f"{self.firstName} {self.lastName}"
    
    @property
    def follower_count(self):
        return self.followers.count()

    @property
    def following_count(self):
        return self.following.count()

    @property
    def bookmarked_posts_count(self):
        return self.bookmarks.count()
    
    @property
    def drafted_posts(self):
        return self.post_user.filter(status='draft')

    @property
    def published_posts(self):
        return self.post_user.filter(status='published')

    
    @property
    def drafted_posts_count(self):
        return self.post_user.filter(status='draft').count()

    @property
    def published_posts_count(self):
        return self.post_user.filter(status='published').count()
    
    @property
    def boosted_posts_count(self):
        return self.boosted_posts.count()

    
def user_directory_path(instance, filename):
    return 'blog/{0}/{1}'.format(instance.slug, filename)

class Post(models.Model):
    class PostObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='published')

    options = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )
    title = models.CharField(max_length=100)
    thumbnail = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
    excerpt = models.CharField(max_length=140, null=True)
    content = models.TextField()
    content_preview = models.CharField(max_length=220)
    slug = AutoSlugField(populate_from='title', unique=True)
    published = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_user')
    status = models.CharField(max_length=10, choices=options, default='draft')
    tags = models.ManyToManyField('Tag', related_name='posts', blank=True)
    boosts = models.ManyToManyField(User, related_name='boosted_posts', blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()
    postobjects = PostObjects()
    

    class Meta:
        ordering = ('-published',)

    def __str__(self):
        return self.title
    
    @property
    def boosts_count(self):
        return self.boosts.count()


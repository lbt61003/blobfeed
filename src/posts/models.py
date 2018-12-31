import re

from django.conf import settings
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.utils import timezone
from django.utils.text import slugify

# Create your models here.
#from hashtags.signals import parsed_hashtags
from .validators import validate_content

def upload_location(instance, filename):
    #filebase, extension = filename.split(".")
    #return "%s/%s.%s" %(instance.id, instance.id, extension)
    Post = instance.__class__
    new_id = Post.objects.order_by("id").last().id + 1
    """
    instance.__class__ gets the model Post. We must use this method because the model is defined below.
    Then create a queryset ordered by the "id"s of each object, 
    Then we get the last object in the queryset with `.last()`
    Which will give us the most recently created Model instance
    We add 1 to it, so we get what should be the same id as the the post we are creating.
    """
    return "%s/%s" %(new_id, filename)

class Post(models.Model):
	parent      = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True)
	user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	title = models.CharField(max_length=120)
	slug = models.SlugField(unique=True)
	image = models.ImageField(upload_to=upload_location, 
		null=True, 
		blank=True, 
		width_field="width_field", 
		height_field="height_field")
	height_field = models.IntegerField(default=0)
	width_field = models.IntegerField(default=0)
    #content = models.TextField()
	#draft = models.BooleanField(default=False)
	#publish = models.DateField(auto_now=False, auto_now_add=False)
	read_time =  models.IntegerField(default=0) # models.TimeField(null=True, blank=True) #assume minutes
	content     = models.CharField(max_length=140, validators=[validate_content])
	liked       = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='liked')
	reply       = models.BooleanField(verbose_name='Is a reply?', default=False)
	updated     = models.DateTimeField(auto_now=True)
	timestamp   = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return str(self.content)

	def get_absolute_url(self):
		return reverse("posts:detail", kwargs={"pk":self.pk})

	class Meta:
		ordering = ['-timestamp']

	def get_parent(self):
		the_parent = self
		if self.parent:
			the_parent = self.parent
		return the_parent

	def get_children(self):
		parent = self.get_parent()
		qs = Post.objects.filter(parent=parent)
		qs_parent = Post.objects.filter(pk=parent.pk)
		return (qs | qs_parent)

	#def clean(self, *args, **kwargs):
	    #     content = self.content
	    #     if content == "abc":
	    #         raise ValidationError("Content cannot be ABC")
	    #     return super(Tweet, self).clean(*args, **kwargs)

def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Post.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" %(slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug



def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

    # if instance.content:
    #     html_string = instance.get_markdown()
    #     read_time_var = get_read_time(html_string)
    #     instance.read_time = read_time_var


pre_save.connect(pre_save_post_receiver, sender=Post)

def post_save_receiver(sender, instance, created, *args, **kwargs):
    if created and not instance.parent:
        # notify a user
        user_regex = r'@(?P<username>[\w.@+-]+)'
        usernames = re.findall(user_regex, instance.content)
        # send notification to user here.

        hash_regex = r'#(?P<hashtag>[\w\d-]+)'
        hashtags = re.findall(hash_regex, instance.content)
        #parsed_hashtags.send(sender=instance.__class__, hashtag_list=hashtags)
        # send hashtag signal to user here.








post_save.connect(post_save_receiver, sender=Post)

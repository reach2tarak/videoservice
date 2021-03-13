from django.db import models
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

SUBSCRIPTION = (
    ('F', 'FREE'),
    ('M', 'MONTHLY'),
    ('Y', 'YEARLY')
)

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_pro = models.BooleanField(default=False)
    pro_expiry_date = models.DateTimeField(null=True, blank=True)
    subscription_type = models.CharField(max_length=100, choices=SUBSCRIPTION, default="FREE")

# Create your models here.
class Course(models.Model):
    course_name = models.CharField(max_length=200)
    course_desc = RichTextField()
    is_premium = models.BooleanField(default=False)
    course_image = models.ImageField(upload_to='course')
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.course_name)
        super(Course, self).save(*args, **kwargs)

    def __str__(self):
        return self.course_name

class CourseModule(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    course_module_name = models.CharField(max_length=100)
    course_description = RichTextField()
    video_ulr = models.URLField(max_length=300)
    can_view = models.BooleanField(default=False)
import helpers
from django.db import models
from cloudinary.models import CloudinaryField

helpers.cloudinary_init()

# Create your models here.
class AccessRequirement(models.TextChoices):
    ANYONE = "any", "Anyone"
    EMAIL_REQUIRED = "email", "Email Required"


class PublishStatus(models.TextChoices):
    PUBLISHED = "pub", "Published"
    COMING_SOON = "soon", "Coming Soon"
    DRAFT = "draft", "Draft"


def handle_upload(instance, filename):
    return f"{filename}"    

class Course(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    # image = models.ImageField(upload_to=handle_upload, blank=True, null=True)
    image = CloudinaryField("image", null=True)
    access = models.CharField(max_length=5, 
                              choices=AccessRequirement.choices, 
                              default=AccessRequirement.EMAIL_REQUIRED
                              )
    status = models.CharField(max_length=10, 
                              choices=PublishStatus.choices, 
                              default=PublishStatus.DRAFT
                              )
    

    @property
    def is_published(self):
        return self.status == PublishStatus.PUBLISHED
    

    @property
    def image_admin_url(self):
        if not self.image:
            return ""
        
        image_options = {
            "width":200
        }

        url = self.image.build_url(**image_options)
        return url
    
    

    def get_image_thumbnail(self, as_html=False, width=500):
        if not self.image:
            return ""
        
        image_options = {
            "width":width
        }
        
        if as_html:
            #CloudinaryImage(str(self.image)).image(**image_options)
            return self.image.image(**image_options) 
        #CloudinaryImage(str(self.image)).build_url(**image_options)
        url = self.image.build_url(**image_options)
        return url
    

    
    def get_image_detail(self, as_html=False, width=750):
        if not self.image:
            return ""
        
        image_options = {
            "width":width
        }
        
        if as_html:
            #CloudinaryImage(str(self.image)).image(**image_options)
            return self.image.image(**image_options) 
        #CloudinaryImage(str(self.image)).build_url(**image_options)
        url = self.image.build_url(**image_options)
        return url
    




class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    thumbnail = CloudinaryField("image", 
                                blank=True, 
                                null=True
                                )
    video = CloudinaryField("video", 
                            blank=True, 
                            null=True, 
                            resource_type="video"
                            )
    preview = models.BooleanField(default=False, 
                                  help_text="if users don't have access to course, can they ses this"
                                  )
    status = models.CharField(max_length=10, 
                              choices=PublishStatus.choices, 
                              default=PublishStatus.PUBLISHED
                              )
    
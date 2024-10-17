from cloudinary import CloudinaryImage
from django.contrib import admin
from django.utils.html import format_html
# Register your models here.
from .models import Course, Lesson

class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 0
    readonly_fields = ['updated']



@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline]
    list_display = ['title', 'status', 'access']
    list_filter = ['status', 'access']
    fields = ['title', 'description', 'status', 'image', 'access', 'display_image']
    readonly_fields = ['display_image']


    def display_image(self, obj, *args, **kwargs):
        url = obj.image_admin_url
        cloudinary_id = str(obj.image) 
        cloudinary_html1 = obj.image.image(width=200)
        cloudinary_html2 = CloudinaryImage(cloudinary_id).image(width=500)
        return format_html(f"<img src={url} />")
    
    display_image.short_description = "Current image"


#admin.site.register(Course, CourseAdmin)
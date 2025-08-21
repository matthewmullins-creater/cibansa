from django.db import models
from main.models import CbCategory,CbTag

# Create your models here.


def upload_courses_image(instance,filename):
    return "".join(["%s%s" % ("courses/", "/"), filename])

class CbCourses(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(CbCategory,on_delete=models.SET_NULL,null=True,related_name="category_courses")
    content = models.TextField()
    image = models.ImageField(default="courses_image.png",upload_to=upload_courses_image)
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="user_courses")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    meta_data = models.JSONField()
    is_visible = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "cb_courses"


# class CbCoursesTags(models.Model):
#     courses = models.ForeignKey(CbCourses, on_delete=models.CASCADE,related_name="courses_tags")
#     tag = models.ForeignKey(CbTag, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     class Meta:
#         db_table = "cb_courses_tags"



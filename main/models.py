from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.


def category_image_path(instance,filename):
    return ""


class CbCategory(models.Model):
    name = models.CharField(max_length=15)
    image = models.ImageField(upload_to=category_image_path,default="default_category_img.png")
    description = models.CharField(max_length=200,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    meta_data = JSONField(null=True,blank=True)

    class Meta:
        db_table="cb_category"

    def __str__(self):
        return self.name

def topic_image_path(instance,filename):
    return ""


class CbTopic(models.Model):
    category = models.ForeignKey(CbCategory,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to=topic_image_path, default="default_topic_img.png")
    description = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    meta_data = JSONField(null=True, blank=True)

    class Meta:
        db_table="cb_topic"

    def __str__(self):
        return "%s -%s" %(self.id,self.name)


class CbTag(models.Model):
    name = models.CharField(max_length=15,unique=True)

    def __str__(self):
        return "%s" %(self.name)

    class Meta:
        db_table="cb_tag"


class CbTopicTags(models.Model):
    topic = models.ForeignKey(CbTopic,on_delete=models.CASCADE)
    tag = models.ForeignKey(CbTag,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s-%s" %(self.topic.title,self.tag.name)

    class Meta:
        db_table = "cb_topic_tags"











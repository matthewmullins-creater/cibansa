from django.db import models
from django.contrib.postgres.fields import JSONField
from autoslug import AutoSlugField
# Create your models here.


def category_image_path(instance,filename):
    return "".join(["%s%s%s" % ("category/", str(instance.name), "/"), filename])


class CbCategory(models.Model):
    name = models.CharField(max_length=255,unique=True)
    image = models.ImageField(upload_to=category_image_path,default="default_category_img.png")
    description = models.CharField(max_length=1024,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey("accounts.User",related_name="user_categories")
    updated_at = models.DateTimeField(auto_now=True)
    slug = AutoSlugField(populate_from="name", max_length=200,always_update=True,unique=True)
    meta_data = JSONField(null=True,blank=True)
    is_visible = models.BooleanField(default=True)

    class Meta:
        db_table="cb_category"

    def __str__(self):
        return self.name



def topic_image_path(instance,filename):
    return "".join(["%s" % "topic/", filename])


class CbTopic(models.Model):
    category = models.ForeignKey(CbCategory,on_delete=models.CASCADE,related_name="category_topics")
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to=topic_image_path, default="default_topic_img.png")
    description = models.CharField(max_length=1024, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey("accounts.User",related_name="user_topic")
    updated_at = models.DateTimeField(auto_now=True)
    slug = AutoSlugField(populate_from="title", max_length=200,always_update=True,unique=True)
    meta_data = JSONField(null=True, blank=True)
    is_visible = models.BooleanField(default=True)

    class Meta:
        db_table="cb_topic"

    def __str__(self):
        return "%s -%s" %(self.category.name,self.title)

    def get_no_of_discussion(self):
        discussion=0
        for q in self.topic_questions.filter(is_deleted=False):
            discussion += q.question_answers.count()
            for k in q.question_answers.all():
                discussion += k.answer_replies.count()

        d = {"discussion":discussion}

        return d

    def get_no_questions(self):
        return self.topic_questions.filter(is_deleted=False).count()


class CbTag(models.Model):
    name = models.CharField(max_length=255,unique=True)
    slug = AutoSlugField(populate_from="name",max_length=200,always_update=True,unique=True)

    def __str__(self):
        return "%s" %(self.name)

    class Meta:
        db_table="cb_tag"


class CbCategoryTags(models.Model):
    category = models.ForeignKey(CbCategory,on_delete=models.CASCADE,related_name="category_tags")
    tag = models.ForeignKey(CbTag,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s-%s" %(self.category.name,self.tag.name)

    class Meta:
        db_table = "cb_category_tags"


class CbTopicTags(models.Model):
    topic = models.ForeignKey(CbTopic,on_delete=models.CASCADE,related_name="topic_tags")
    tag = models.ForeignKey(CbTag,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s-%s" %(self.topic.title,self.tag.name)

    class Meta:
        db_table = "cb_topic_tags"


class CbQuestion(models.Model):
    topic = models.ForeignKey(CbTopic,on_delete=models.CASCADE,related_name="topic_questions")
    category = models.ForeignKey(CbCategory, on_delete=models.CASCADE, related_name="category_questions")
    title = models.CharField(max_length=1024)
    description = models.TextField()
    owner = models.ForeignKey("accounts.User", related_name="user_questions")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    slug = AutoSlugField(populate_from="title", max_length=200,always_update=True,unique=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return "%s..." % self.title[:1024]

    class Meta:
        db_table = "cb_question"


class CbQuestionTag(models.Model):
    question = models.ForeignKey(CbQuestion, on_delete=models.CASCADE,related_name="question_tags")
    tag = models.ForeignKey(CbTag, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s-%s" % (self.question.title, self.tag.name)

    class Meta:
        db_table = "cb_question_tags"


class CbAnswer(models.Model):
    user = models.ForeignKey("accounts.User",related_name="user_answer")
    question = models.ForeignKey(CbQuestion, on_delete=models.CASCADE,related_name="question_answers")
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "cb_answer"


class CbAnswerReply(models.Model):
    answer = models.ForeignKey(CbAnswer,on_delete=models.CASCADE,related_name="answer_replies")
    comment = models.TextField()
    user = models.ForeignKey("accounts.User")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "cb_answer_reply"


class CbAnswerLike(models.Model):
    answer = models.ForeignKey(CbAnswer, on_delete=models.CASCADE,related_name="answer_likes")
    user = models.ForeignKey("accounts.User")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "cb_answer_like"
        unique_together = (("answer","user"),)


class CbAnswerReplyLike(models.Model):
    answer_reply = models.ForeignKey(CbAnswerReply, on_delete=models.CASCADE,related_name="answer_reply_likes")
    user = models.ForeignKey("accounts.User")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "cb_answer_reply_like"
        unique_together = (("answer_reply", "user"),)








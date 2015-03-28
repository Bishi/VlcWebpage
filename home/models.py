from django.db import models
from time import time
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def get_upload_file_name(instance, filename):
    return "uploaded_files/%s_%s" % (str(time()).replace('.','_'), filename)


class NewsArticle(models.Model):
    #image size limit
    def validate_image(self):
        file_size = self.file.size
        megabyte_limit = 5.0
        if file_size > megabyte_limit*1024*1024:
            raise ValidationError("Max file size is %sMB" % str(megabyte_limit))

    title = models.CharField(max_length=30)
    body = models.TextField(max_length=9000, blank=True)
    pub_date = models.DateTimeField('date published')
    likes = models.IntegerField(default=0)
    thumbnail = models.ImageField(upload_to=get_upload_file_name, null=True, blank=True, validators=[validate_image])
    author = models.ForeignKey('auth.User')

    def __str__(self):
        return self.title


class ClassName(models.Model):
    class_name_text = models.CharField(max_length=20)
    pic = models.FileField(upload_to="class_thumbnails/")

    def __str__(self):
        return self.class_name_text


class ClassRole(models.Model):
    class_role_text = models.CharField(max_length=20)

    def __str__(self):
        return self.class_role_text


class Recruitment(models.Model):
    class_name = models.ForeignKey(ClassName)
    class_role = models.ForeignKey(ClassRole)
    #class_text = models.CharField(max_length=30)
    #name = class_name.class_name_text

    def __str__(self):
        return self.class_name.class_name_text
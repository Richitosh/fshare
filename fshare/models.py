# -*- coding: utf-8 -*-
from django.db import models
from django.forms import ModelForm
import os.path

def get_file_name(instance, filename):
    return os.path.join('.', '{0:07d}'.format(instance.fileset.id), filename)


class Creator(models.Model):
    full_name = models.CharField(max_length=80)
    appointment = models.CharField(max_length=80) # должность
    department = models.CharField(max_length=80)  # филиал
    email = models.CharField(max_length=30)
    phone = models.CharField(max_length=100)

    class Meta:
        unique_together = (('full_name', 'appointment','department'),)

    def __unicode__(self):
        return self.full_name


class FileSet(models.Model):
    LIVE_TIMES = (
        (300,'5 минут'),    # Как здесь решить проблему выбора нескольких
        (600,'10 минут'),   # языков (?)
        (3600,'1 час'),
        (10800,'3 часа'),
        (28800,'8 часов'),
        (86400,'1 сутки'),
        (259200,'3 суток'),
        (604800,'7 суток'),
        (2678400,'1 месяц'),
    )
    
    pub_date = models.DateTimeField(auto_now=True)
    end_date = models.DateTimeField()
    # live_time оставлено для удобства, чтобы было видно, на сколько выложили
    live_time = models.PositiveIntegerField(choices=LIVE_TIMES,
                                            default=LIVE_TIMES[7][0])
    creator = models.ForeignKey('Creator')
    password = models.CharField(max_length=80, blank=True) # удалить, id вместо него
    description = models.TextField(blank=True)
    total_size = models.PositiveIntegerField() # удалить, всегда доступно


    def __unicode__(self):
        return ''.join(['{0:07d}'.format(self.id), ' [',str(self.pub_date), '] ',
                  str(self.live_time/3600), ' hour(s)'])


class File(models.Model):
    file_name = models.CharField(max_length=100)
    # файл не удаляется автоматически при удалении объекта
    file = models.FileField(upload_to=get_file_name)
    file_size = models.BigIntegerField() # удалить, всегда доступно
    fileset = models.ForeignKey('FileSet')

    def __unicode__(self):
        return self.file_name[:100]

# model forms
class CreatorForm(ModelForm):
    class Meta:
        model = Creator


class FileForm(ModelForm):
    class Meta:
        model = File
        #exclude = ('file_name', 'file_size', 'file_set',)


class FileSetForm(ModelForm):
    class Meta:
        model = FileSet
        exclude = ('pub_date', 'end_date', 'creator', 'total_size', 'password',)


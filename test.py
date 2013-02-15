#!/usr/bin/python
# -*- coding: utf-8 -*-
from random import randint

from django.conf import settings
settings.configure(
    DATABASE_ENGINE = 'sqlite3',
    DATABASE_NAME = '/tmp/timefield_test.sqlite',
)
from django.db import models


def main():
    create_table(Test)
    Test.objects.all().delete()
    
    for i in xrange(10):
        Test().save()
    
    all = Test.objects.all()
    print [obj.id for obj in all.order_by('time')]
    print [obj.id for obj in all.order_by('-time')]
    
    for i in xrange(100):
        id1 = randint(1, 10)
        id2 = randint(1, 10)
        obj1 = Test.objects.get(pk=id1)
        obj2 = Test.objects.get(pk=id2)
        assert (id1 > id2) == (obj1.time > obj2.time)
        print '+',


class Test(models.Model):
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = ''


def create_table(cls):
    from django.db import connection
    from django.core.management.color import no_style
    
    sql, references = connection.creation.sql_create_model(cls, no_style())
    cursor = connection.cursor()
    for q in sql:
        try:
            cursor.execute(q)
        except:
            pass
    

if __name__ == "__main__":
    main()
    
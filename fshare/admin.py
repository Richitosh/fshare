# -*- coding: utf-8 -*-
from django.contrib import admin
from fshare.models import FileSet, Creator, File

admin.site.register(FileSet)
admin.site.register(Creator)
admin.site.register(File)

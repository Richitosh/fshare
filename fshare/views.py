# -*- coding: utf-8 -*-
from django.core.urlresolvers import reverse
from django.http import Http404, HttpRequest, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django import forms
from django.forms.models import modelformset_factory
from fshare.models import *
import datetime
import random

def index_page(request, **kwargs):
    creator_id = 1 # id = 1 - неизвестный пользователь
    files_count = 0
    if request.method == 'POST':
        # обработка создания/выбора creator -->
        creator = None
        creator_form = CreatorForm(request.POST)
        try:
            # проверка существует creator или нет
            creator = Creator.objects.get(
                        full_name=request.POST['full_name'],
                        appointment=request.POST['appointment'],
                        department=request.POST['department'])
            # заполнить форму, ранее внесенными данными
            # todo: добавить галочку "обновить информацию в справочнике"
            #       это будет удалять объект и создавать новый если он
            #       правильно заполнен
            creator_form = CreatorForm(instance=creator)
        except Creator.DoesNotExist:
            # Creator не существует или ошибочно заполнен
            if creator_form.is_valid():
                # в inst.id - id созданного creator'а
                inst = creator_form.save();
                creator = inst
                inst = None
        # обработка создания/выбора creator <--

        # для того чтобы не вводить еще раз пользователя
        if creator: request.session['creator'] = creator.id

        # обработка создания fileset -->
        fileset_form = FileSetForm(request.POST)

        # для проверки ниже, если по ошибке не создастся fileset, то
        # нечего будет удалять, а если он создатся, но будут неправильные
        # файлы, то его надо удалить, а создавать его нужно заранее
        # т.к. от него зависит модель File
        fileset = None
        
        if fileset_form.is_valid() and creator:
            # не должно быть возможности попадания на существующий fileset
            inst = fileset_form.save(commit=False)

            # генерирование случайного номера fileset, если не удалось
            # выбирается по умолчанию
            random.seed()
            for i in xrange(1,10):
                rand_id = random.randint(100000,999000)
                if not FileSet.objects.filter(id=rand_id):
                    break
                else:
                    rand_id = 0
            
            if rand_id: inst.id = rand_id
            
            # интерфейс администратора в браузере работает по времени системы
            # т.е. при обновлении времени часовой пояс может не совпасть
            inst.pub_date = datetime.datetime.now()
            inst.end_date = datetime.datetime.now() + datetime.timedelta(
                        seconds=int(fileset_form.cleaned_data['live_time']))
            inst.creator = creator
            inst.total_size = 0
            inst = fileset_form.save(commit=True)
            fileset = inst
            inst = None
        # обработка создания fileset <--


        # обработка создания file -->
        # Formset для файлов, т.к. их может быть несколько
        file_form = modelformset_factory(File,
                                         form=FileForm,
                                         fields=('file',),
                                         max_num=5,
                                         extra=3)
        file_form = file_form(request.POST, request.FILES)
        insts = file_form.save(commit=False)
        files_count = len(insts)
        
        if file_form.is_valid() and fileset and creator and len(insts):
            # если выбран хотя бы один файл
            # todo: добавить проверки на повторяющиеся,
            #       удаленные в процессе загрузки файлы
            for inst in insts:
                inst.fileset = fileset
                # получить имя файла, размер
                inst.file_size = 0
                inst.file_name = str(inst.file)
                inst.save()
            return HttpResponseRedirect(reverse('success_upload',
                                                kwargs={'fileset':fileset.id}))
        else:
            # удалить пустой fileset
            if fileset: fileset.delete()

        # обработка создания file <--

    else:
        creator = Creator.objects.get(id=request.session.get('creator', 1))
        creator_form = CreatorForm(instance=creator)
        fileset_form = FileSetForm()
        #file_form = FileForm()  #request.POST, request.FILES
        file_form = modelformset_factory(File, form=FileForm, fields=('file',),
                                         max_num=5, extra=5)
        # чтобы не показывать существующие данные надо сделать нулевую выборку
        file_form = file_form(queryset=File.objects.none())


    
    return render_to_response('index.html',
                              {'file_form': file_form,
                              'fileset_form': fileset_form,
                              'creator_form': creator_form,
                              'files_count': files_count,
                              'request': request},
                              context_instance=RequestContext(request)
                            )

def success_upload(request, **kwargs):
    # сообщение об успешной загрузке файла

    fileset_id = int(kwargs['fileset'])
    download_path = request.build_absolute_uri(
                                            reverse('download',
                                            kwargs={'fileset':fileset_id}))

    fileset = FileSet.objects.get(id=fileset_id)
    return render_to_response('success_upload.html',
                              {'download_path': download_path,
                              'fileset': fileset,
                              'request': request})

def download(request, **kwargs):
    # скачивание файлов
    fileset_id = int(kwargs['fileset'])

    # получение всех объектов
    fileset = FileSet.objects.get(id=fileset_id)
    creator = fileset.creator
    files = File.objects.filter(fileset=fileset)
    
    
    
    return render_to_response('download.html',
                              {'fileset': fileset_id,
                              'request': request,
                              'fileset': fileset,
                              'creator': creator,
                              'files': files,
                              })
    






    
import re
from django.shortcuts import render, redirect
from django.http import StreamingHttpResponse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from .models import Task
from .drivedown_api import get_response

page_size = 10
page_n_neighbours = 5


def index(request):
    return render(request, 'index.html')


def new(request):
    drivetype = request.POST.get('drivetype', None)
    url = request.POST.get('url', None)
    ip = request.META['REMOTE_ADDR']

    r = get_response(drivetype, url)
    if not r or 'Content-Disposition' not in r.headers or 'filename' not in r.headers['Content-Disposition']:
        return render(request, 'error.html', {'message': 'URL error'})
    size = int(r.headers['Content-Length']) if 'Content-Length' in r.headers else None
    r.close()

    task = Task(drivetype=drivetype, url=url, size=size, ip=ip)
    task.save()

    return redirect(download, id=task.id)


def download(request, id):
    try:
        task = Task.objects.get(id=id)
    except:
        return render(request, 'error.html', {'message': 'ID error'})

    return render(request, 'download.html', {
        'task': task
    })


def get(request, id):
    try:
        task = Task.objects.get(id=id)
    except:
        return render(request, 'error.html', {'message': 'ID error'})

    if not task.confirmed:
        return render(request, 'error.html', {'message': "Please wait for administrator's confirmation"})

    r = get_response(task.drivetype, task.url)
    response = StreamingHttpResponse(r)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="%s"' % re.search('filename="(.*)"', r.headers['Content-Disposition']).group(1)
    size = task.size
    if size:
        response['Content-Length'] = size
    return response


def list(request):
    page = request.GET.get('page')
    paginator = Paginator(Task.objects.all().order_by('-id'), page_size)
    try:
        tasks = paginator.page(page)
    except PageNotAnInteger:
        tasks = paginator.page(1)
    except InvalidPage:
        return render(request, 'error.html', {'message': 'Page number error'})
    except EmptyPage:
        tasks = paginator.page(paginator.num_pages)

    left = tasks.number - page_n_neighbours if tasks.number - page_n_neighbours > 1 else 1
    right = tasks.number + page_n_neighbours if tasks.number + page_n_neighbours < paginator.num_pages else paginator.num_pages
    return render(request, 'list.html', {
        'tasks': tasks,
        'range': range(left, right+1)
    })


def confirm(request, id):
    try:
        task = Task.objects.get(id=id)
    except:
        return render(request, 'error.html', {'message': 'ID error'})

    task.confirmed = True
    task.save()

    if 'HTTP_REFERER' in request.META:
        return redirect(request.META['HTTP_REFERER'])
    else:
        return redirect(list)

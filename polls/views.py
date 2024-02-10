from django.http import HttpResponse
import re

def natural_sort(objects_list, sort_key):
    """ Sort a list of objects by a given key
    This function sort a list of objects by a given
    key common across the objects
    Sorting can be implemented on keys that are either
    alphabets, integers or both
    """
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [
        convert(c) for c in re.split("([0-9]+)", getattr(key, sort_key))
    ]
    return sorted(objects_list, key=alphanum_key)

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

# parsing data from the client
from rest_framework.parsers import JSONParser
# To bypass having a CSRF token
from django.views.decorators.csrf import csrf_exempt
# for sending response to the client
from django.http import HttpResponse, JsonResponse
# API definition for task
from .serializers import TaskSerializer
# Task model
from .models import Task
#Pagination
from django.core.paginator import Paginator


@csrf_exempt
def tasks(request):
    '''
    List all task snippets
    '''
    if(request.method == 'GET'):
        # get all the tasks
        tasks = natural_sort(Task.objects.all(), 'title')


        # Set up Pagination
        page = request.GET.get('page') or 1
        pageSize = request.GET.get('pageSize') or 10
        
        pages = Paginator(tasks, pageSize)
        data = pages.get_page(page)
        # serialize the task data
        serializer = TaskSerializer(data, many=True)
        info = {
            'data': serializer.data,
            'count': data.paginator.count,
            'num_pages': data.paginator.num_pages,
            'per_page': data.paginator.per_page,
            'current_page': data.number,
            'has_previous': data.has_previous(),
            'has_next': data.has_next(),
            'start_index': data.start_index(),
            'end_index': data.end_index(),
            'has_other_pages': data.has_other_pages(),
        }

        # return a Json response
        return JsonResponse(info,safe=False)
    elif(request.method == 'POST'):
        # parse the incoming information
        data = JSONParser().parse(request)
        # instanciate with the serializer
        serializer = TaskSerializer(data=data)
        # check if the sent information is okay
        if(serializer.is_valid()):
            # if okay, save it on the database
            serializer.save()
            # provide a Json Response with the data that was saved
            return JsonResponse(serializer.data, status=201)
            # provide a Json Response with the necessary error information
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def task_detail(request, pk):
    try:
        # obtain the task with the passed id.
        task = Task.objects.get(pk=pk)
    except:
        # respond with a 404 error message
        return HttpResponse(status=404)  
    if(request.method == 'GET'):
        # get all the tasks
        serializer = TaskSerializer(task, many=False)
        return JsonResponse(serializer.data,safe=False)
    if(request.method == 'PUT'):
        # parse the incoming information
        data = JSONParser().parse(request)  
        # instanciate with the serializer
        serializer = TaskSerializer(task, data=data)
        # check whether the sent information is okay
        if(serializer.is_valid()):  
            # if okay, save it on the database
            serializer.save() 
            # provide a JSON response with the data that was submitted
            return JsonResponse(serializer.data, status=201)
        # provide a JSON response with the necessary error information
        return JsonResponse(serializer.errors, status=400)
    elif(request.method == 'DELETE'):
        # delete the task
        task.delete() 
        # return a no content response.
        return HttpResponse(status=204) 
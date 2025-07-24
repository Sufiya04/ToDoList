from django.shortcuts import render
from django.http import HttpResponse
from .forms import *
from .models import *
# Create your views here.
def add(request):
    return render(request,'add.html')
def display_task(request):
    if request.method=='POST':
        todo=TodoList(request.POST)
        if todo.is_valid():
            t=todo.cleaned_data['task']
            d=todo.cleaned_data['des']
            obj=Todo(task=t,des=d)
            obj.save()
            return HttpResponse("Added Successfully")
        else:
            return HttpResponse("Invalid Task")
            # return render(request,'add.html',{'data':todo})
    else:
        todo=TodoList()
        print("Invalid Response")
        return render(request,'add.html',{'data':todo})
def view(request):
            todo=Todo.objects.all()
            return render(request,'view.html',{'all':todo})
def update(request,id):
    todo=Todo.objects.get(id=id)
    # if request.method=='POST':
    #     t=request.POST['task']
    #     d=request.POST['des']
    #     obj=Todo(task=t,des=d)
    #     obj.save()
    #     return HttpResponse("Updated Successfully")
    # else:
    return render(request,'update.html',{'tsk':todo})
def delete(request,id):
    todo=Todo.objects.get(id=id)
    todo.delete()
    return render(request,'view.html')
     

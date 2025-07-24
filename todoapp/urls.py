from django.urls import path
from .views import *
urlpatterns=[
    path('add',display_task),
    path('view',view,name='view'),
    path('update/<int:id>',update,name='update'),
    path('delete/<int:id>',delete,name='delete')
]
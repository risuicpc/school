from django.urls import path
from .views import *

app_name = 'staff'
urlpatterns = [
    # Grade
    path('grade/list/', GradeListView.as_view(), name='list'),
    path('grade/create/', GradeCreateView.as_view(), name='create'),
    path('grade/<int:id>/edit/', GradeUpdateView.as_view(), name='edit'),
    path('grade/<int:id>/delete/', GradeDeleteView.as_view(), name='delete'),

    # Subject
    path('subject/list/', SubjectListView.as_view(), name='s-list'),
    path('subject/create/', SubjectCreateView.as_view(), name='s-create'),
    path('subject/<int:id>/edit/', SubjectUpdateView.as_view(), name='s-edit'),
    path('subject/<int:id>/delete/', SubjectDeleteView.as_view(), name='s-delete'),

    # Room
    path('room/list/', RoomListView.as_view(), name='r-list'),
    path('room/create/', RoomCreateView.as_view(), name='r-create'),
    path('room/<int:id>/edit/', RoomUpdateView.as_view(), name='r-edit'),
    path('room/<int:id>/delete/', RoomDeleteView.as_view(), name='r-delete'),

    # Teach
    path('teach/list/', TeachListView.as_view(), name='t-list'),
    # path('teach/create/', TeachCreateView.as_view(), name='t-create'),
    path('teach/<int:id>/edit/', TeachUpdateView.as_view(), name='t-edit'),
    path('teach/<int:id>/delete/', TeachDeleteView.as_view(), name='t-delete'),

   
]

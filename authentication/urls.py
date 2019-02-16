from django.urls import path
from .views import (
    user_create, user_exel, user_list, user_update, user_delete, user_profile, user_profile_edit
)

urlpatterns = [
    path('', user_list, name='list'),
    path('create/', user_create, name='create'),
    path('user_exel/', user_exel, name='user-exel'),
    path('<int:id>/edit/', user_update, name='edit'),
    path('<int:id>/delete/', user_delete, name='delete'),
    path('profile/', user_profile, name='profile'),
    path('profile/edit/', user_profile_edit, name='editprofile'),

    # Class based view
    # path('register/', CreateView.as_view(), name='register'),
    # path('user/', UserListView.as_view(), name='user'),
]

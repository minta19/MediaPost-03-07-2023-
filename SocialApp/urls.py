from django.urls import path
from .import views

urlpatterns=[
    path('home/',views.home,name='home'),
    path('dashboard/',views.post_list,name='dashboard'),
    path('createpost/',views.create_post,name='create'),
    path('delete/<uuid:post_id>/', views.delete_post, name='deletepost'),
    path('edit/<uuid:post_id>/', views.edit_post, name='editpost'),

    path('login/',views.userLogin,name='login'),
    path('signup/',views.signup,name='signup'),

]
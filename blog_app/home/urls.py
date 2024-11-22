from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('',views.PostListView.as_view(),name='home'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',views.post_details,name='details'),
    path('add/', views.add_post, name='add_post'),
    path('delete/<int:id>/', views.delete_post, name='delete_post'),
    path('update/<int:id>',views.update_post,name = 'update_post'),
]


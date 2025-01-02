from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('',views.posts_list , name='home'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',views.post_details,name='details'),
    path('add/', views.add_post, name='add_post'),
    path('delete/<int:id>/', views.delete_post, name='delete_post'),
    path('update/<int:id>/',views.update_post,name = 'update_post'),
    path('share/<int:post_id>/', views.share_post, name= 'share_post'),
    path('comment/<int:post_id>/', views.comment_post, name= 'comment_post'),
    path('tag/<slug:tag_slug>/', views.posts_list, name='posts_by_tag'),
    path('search/', views.search, name='search'),
]


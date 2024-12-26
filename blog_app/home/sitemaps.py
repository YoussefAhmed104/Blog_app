from django.contrib.sitemaps import Sitemap
# from django.urls import reverse
from .models import Post

class PostSitemap(Sitemap):
    changefreq = "weekly"   # معدل تغير الصفحه(مثلا اسبوعيا)
    priority = 0.9              # الاولويه او الاهميه بالنسبه لبقاي الصفحات (من 0.0 الى 1.0)

    def items(self):    
        return Post.objects.all()     

    def lastmod(self, obj):
        return obj.updated   # تاريخ اخر تعديل على الصفحه


from django.shortcuts import render , get_object_or_404
from .models import Post
from .forms import *
from django.core.paginator import Paginator

def posts_list(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 3)  # استخدم posts بدلاً من posts_list
    page_num = request.GET.get('page', 1)  # الحصول على رقم الصفحة من الرابط أو تعيين الصفحة الأولى كافتراضي
    page_obj = paginator.page(page_num)  # استخدم paginator بدلاً من Paginator مباشرة
    return render(request, 'home.html', {'posts': page_obj})

def post_details(request, year, month, day, post):
    post = get_object_or_404(Post, 
                            slug=post,
                            publish__year=year,
                            publish__month=month,
                            publish__day=day)
    return render(request , 'details.html',{'post':post})

# views.py
from django.shortcuts import render, redirect
from .forms import PostForm

def add_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/')  # يمكنك تعديل هذا الرابط إلى اسم الصفحة التي تريد الانتقال إليها بعد الحفظ
    else:
        form = PostForm()  # إنشاء نموذج فارغ عند طلب الصفحة عبر GET

    return render(request, 'pages/add.html', {'form': form})


def delete_post(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        post.delete()  # حذف المنشور من قاعدة البيانات
        return redirect('blog:home')  # إعادة التوجيه إلى الصفحة الرئيسية بعد الحذف
    return render(request, 'blog/delete_post.html', {'post': post})



def update_post(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)  # تمرير الكائن لملء الحقول
        if form.is_valid():
            form.save()  # حفظ التعديلات
            return redirect('blog:home')  # إعادة توجيه إلى صفحة التفاصيل بعد التحديث
    else:
        form = PostForm(instance=post)  # ملء الحقول بالبيانات الحالية في حالة GET

    return render(request, 'pages/update.html', {'form': form, 'post': post})

from django.shortcuts import render , get_object_or_404,redirect
from .models import Post
from .forms import *
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.views.generic import ListView


# def posts_list(request):#بنستخدم الباجيناتور علشان نعمل حد للبوستات الي تظهرلك
#     posts = Post.objects.all()
#     paginator = Paginator(posts, 3)  # استخدم posts بدلاً من posts_list
#     page_num = request.GET.get('page', 1)  # الحصول على رقم الصفحة من الرابط أو تعيين الصفحة الأولى كافتراضي
#     try:
#         page_obj = paginator.page(page_num)  # استخدم paginator بدلاً من Paginator مباشرة
#     except EmptyPage:
#         page_obj = paginator.page(paginator.num_pages) #علشان ميجبلكش خطأ 
#     except PageNotAnInteger:#علشان او في حروف مكان الاي دي ميجيش غلط و هيجيبلك اول صفحه 
#         page_obj = paginator.page(1)
#     return render(request, 'home.html', {'posts': page_obj})


class PostListView(ListView):
    """
    Alternative post list view
    """
    model = Post        #==# posts = Post.objects.all()
    context_object_name = 'posts'   #this is a context like this {'posts': page_obj}
    paginate_by = 3     #==# paginator = Paginator(posts, 3)
    template_name = 'home.html'    #==#return render(request, 'home.html', {'posts': page_obj})
    

def post_details(request, year, month, day, post):#علشان اخلي الايدي بالسنه و الشهر و اليوم و ف الاخر الايدي بتاع البوست
    post = get_object_or_404(Post, 
                            slug=post,
                            publish__year=year,
                            publish__month=month,
                            publish__day=day)
    return render(request , 'details.html',{'post':post})


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

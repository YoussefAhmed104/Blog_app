from django.shortcuts import render , get_object_or_404,redirect
from .models import Post
from .forms import *
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.views.generic import ListView
from django.core.mail import send_mail
from django.views.decorators.http import require_POST
from django.db.models import Count
from taggit.models import Tag
from django.contrib.postgres.search import SearchVector , SearchQuery , SearchRank



def posts_list(request, tag_slug=None):#بنستخدم الباجيناتور علشان نعمل حد للبوستات الي تظهرلك
    posts = Post.objects.annotate(num_comments=Count('comments')).order_by('created')

    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag , slug= tag_slug)
        posts = posts.filter(tags__in=[tag])

    paginator = Paginator(posts, 5)  # استخدم posts بدلاً من posts_list
    page_num = request.GET.get('page', 1)  # الحصول على رقم الصفحة من الرابط أو تعيين الصفحة الأولى كافتراضي
    try:
        page_obj = paginator.page(page_num)  # استخدم paginator بدلاً من Paginator مباشرة
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages) #علشان ميجبلكش خطأ 
    except PageNotAnInteger:#علشان او في حروف مكان الاي دي ميجيش غلط و هيجيبلك اول صفحه 
        page_obj = paginator.page(1)
        
    return render(request, 'home.html', {'posts': page_obj , 'tag':tag})


#class based vies

# class PostListView(ListView):
#     """
#     Alternative post list view
#     """
#     model = Post        #==# posts = Post.objects.all()
#     context_object_name = 'posts'   #this is a context like this {'posts': page_obj}
#     paginate_by = 3     #==# paginator = Paginator(posts, 3)
#     template_name = 'home.html'    #==#return render(request, 'home.html', {'posts': page_obj})
    

def post_details(request, year, month, day, post):#علشان اخلي الايدي بالسنه و الشهر و اليوم و ف الاخر الايدي بتاع البوست
    post = get_object_or_404(Post, 
                            slug=post,
                            publish__year=year,
                            publish__month=month,
                            publish__day=day)
    comments = post.comments.all()
    form = CommentForm()

    post_tags_ids =  post.tags.values_list('id', flat=True)  #بيجيب كل الايديهات بتاعت التاجز الي ع البوست

    similer_posts = Post.objects.filter(tags__in=post_tags_ids).exclude(id=post.id) #بنجيب كل البوستات الي فيهم تاجات شبه بعض

    similer_posts = similer_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','publish')  #علشان يجبلك البوستات الي فيها اكتر من تاج شبه بعض الاول

    return render(request , 'details.html',{'post':post , 'comments':comments ,'similer_posts':similer_posts})
    


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




def share_post(request,post_id):
    post = get_object_or_404(Post, id = post_id , status = Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            supject = f"{cd['name']} recommends you read {post.title}"
            massege = f"read {Post.title} at {post_id} \n {cd['name']}\'s comments: {cd['comments']}"
            send_mail(supject, massege , 'youssifahmed104@gmail.com',[cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request , 'pages/share.html', {'post':post , 'form':form, 'sent':sent})



@require_POST
def comment_post(request,post_id):
    post = get_object_or_404(Post , id=post_id , status = Post.Status.PUBLISHED)
    comment = None
    # A comment was posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # creat a comment object without saving in the database
        comment = form.save(commit=False)
        # assign the post to the comment
        comment.post = post
        #s save the comment to the data base 
        comment.save()
    return render(request , 'pages/comment.html', {'post':post , 'form':form, 'comment':comment})



def search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']  # استخراج البحث من النموذج
            search_vector = SearchVector('title', 'body')
            search_query = SearchQuery(query, config='english')#بنعمل البحث عن الكلمات الي انت كاتبها ف البوست و بنجيب النتيجه الي تحتوي علي الكلمه الي انت كاتبها
            results = Post.objects.annotate(search=search_vector, rank=SearchRank(search_vector, search_query)).filter(search=query).order_by('-rank')  #بنجيب البوستات الي فيها الكلمه الي انت كاتبها و بنرتبها بحسب الاهميه
    return render(request, 'pages/search.html', {'form': form, 'query': query, 'results': results})
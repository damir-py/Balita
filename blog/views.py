import requests
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from .models import Post, Category, Tag, Contact, Comment

BOT_TOKEN = '6787403849:AAE2piymBY7F-9DCRKbEK3kZoBx1paVSTog'
CHAT_ID = '654348985'


def home_view(request):
    categories = Category.objects.all()
    posts = Post.objects.filter(is_published=True)
    tags = Tag.objects.all()
    page_obj = Paginator(posts, 4)
    page = request.GET.get('page', 1)

    cont = {
        'cat_post'
        'posts': posts,
        'latest_posts': posts.order_by('-created_at')[:3],
        'banners': posts[:3],
        'categories': categories,
        'tags': tags,
        # 'posts_page': posts.order_by('created_at'),
        'popular_posts': posts.order_by('-comments_count')[:3],
        'home': 'active',
        'posts_page': page_obj.get_page(page),
    }
    return render(request, 'index.html', context=cont)


def category_view(request):
    categories = Category.objects.all()
    data = request.GET
    cat = data.get('cat', None)
    tags = Tag.objects.all()
    posts = Post.objects.filter(is_published=True)
    cont = {
        'category_act': 'active',
        'cat_posts': posts.filter(category_id=cat),
        'posts': posts,
        'latest_posts': posts.order_by('-created_at')[:3],
        'popular_posts': posts.order_by('-comments_count')[:3],
        'tags': tags,
        'categories': categories,
    }
    return render(request, 'category.html', context=cont)


def about_view(request):
    categories = Category.objects.all()
    posts = Post.objects.filter(is_published=True)
    tags = Tag.objects.all()
    page_obj = Paginator(posts, 2)
    page = request.GET.get('page', 1)

    cont = {
        'about': 'active',
        'categories': categories,
        'latest_posts': posts.order_by('-created_at')[:3],
        'popular_posts': posts.order_by('-comments_count')[:3],
        'tags': tags,
        'posts_page': page_obj.get_page(page)
    }
    return render(request, 'about.html', context=cont)


def contact_view(request):
    if request.method == 'POST':
        data = request.POST
        obj = Contact.objects.create(name=data['name'], phone_number=data['phone'], email=data['email'],
                                     message=data['message'])
        obj.save()
        text = f"""\n
        Project: Balita 👋
ID:{obj.id}
name: {obj.name}
Phone_number: {obj.phone_number} 
timestamp: {obj.created_at.date()}
message: {obj.message}
        """
        url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={text}'
        response = requests.get(url)
        print(response)
        return redirect('/contact')

    posts = Post.objects.filter(is_published=True)
    categories = Category.objects.all()
    tags = Tag.objects.all()
    cont = {
        'contact': 'active',
        'categories': categories,
        'latest_posts': posts.order_by('-created_at')[:3],
        'popular_posts': posts.order_by('-comments_count')[:3],
        'tags': tags,
    }

    return render(request, 'contact.html', context=cont)


def blog_detail_view(request, pk):
    post = Post.objects.get(id=pk)
    if request.method == 'POST':
        data = request.POST
        obj = Comment.objects.create(post=post, name=data['name'], email=data['email'], message=data['message'],
                                     post_id=pk)
        obj.save()
        post.comments_count += 1
        post.save(update_fields=['comments_count'])
        return redirect(f'/blog/{pk}/')

    data = request.GET
    cat = data.get('cat', None)

    post.views_count += 1
    post.save(update_fields=['views_count'])
    comments = Comment.objects.filter(post_id=pk, is_visible=True)
    categories = Category.objects.all()
    posts = Post.objects.filter(is_published=True)
    tags = Tag.objects.all()
    contx = {
        'post': post,
        'cat_post': posts.filter(category_id=cat)[:3],
        'categories': categories,
        'comments': comments,
        'comments_count': len(comments),
        'latest_posts': posts.order_by('-created_at')[:3],
        'popular_posts': posts.order_by('-comments_count')[:3],
        'tags': tags,
    }
    return render(request, 'blog-single.html', context=contx)


def tags_view(request, pk):
    posts = Post.objects.filter(is_published=True)
    categories = Category.objects.all()

    context = {
        'posts': posts.filter(tags__id=pk),
        'categories': categories,
        'latest_posts': posts.order_by('-comments_count')[:3],
    }
    return render(request, 'tags.html', context=context)


def search_view(request):
    tags = Tag.objects.all()
    if request.method == 'POST':
        data = request.POST
        query = data['query']
        return redirect(f'/search?q={query}')
    query = request.GET.get('q')
    if query is not None and len(query) >= 1:
        posts = Post.objects.filter(is_published=True, title__icontains=query, description__icontains=query)
    else:
        posts = Post.objects.filter(is_published=True)

    ls_post = Post.objects.filter(is_published=True)

    d = {'cat_posts': posts,
         'categories': Category.objects.all(),
         'latest_posts': ls_post.order_by('views_count')[:3],
         'tags': tags,

         }

    return render(request, 'category.html', context=d)

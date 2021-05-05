from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404

from .forms import PostForm
from .models import Post, Group


def index(request):
    post_list = Post.objects.order_by('-pub_date').all()
    paginator = Paginator(post_list, 10)  # показывать по 10 записей на странице.

    page_number = request.GET.get('page')  # переменная в URL с номером запрошенной страницы
    page = paginator.get_page(page_number)  # получить записи с нужным смещением
    return render(
        request,
        'index.html',
        {'page': page,
         'paginator': paginator,
         'post_list': post_list,
         }
    )

def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = Post.objects.filter(group=group).order_by("-pub_date")[:10]
    context = {"group": group, "posts": posts}
    return render(
        request,
        'group.html',
        context
    )

def posts(request):
    if request.user.is_authenticated == False:
        return redirect('signup')
    elif request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('index')

    form = PostForm()

    return render(request, 'post.html', {'form': form})


def profile(request, username):
    prof = Post.objects.filter(author__username=username).order_by('-pub_date').all()
    paginator = Paginator(prof, 10)  # показывать по 10 записей на странице.
    page_number = request.GET.get('page')  # переменная в URL с номером запрошенной страницы
    page = paginator.get_page(page_number)  # получить записи с нужным смещением
    return render(
        request,
        'profile.html',
        {'page': page,
         'paginator': paginator,
         'prof': prof,
         }
    )


def post_view(request, username, post_id):
    # тут тело функции
    return render(request, 'post_view.html', {})


def post_edit(request, username, post_id):
    # тут тело функции. Не забудьте проверить,
    # что текущий пользователь — это автор записи.
    # В качестве шаблона страницы редактирования укажите шаблон создания новой записи
    # который вы создали раньше (вы могли назвать шаблон иначе)

    if request.user.username != username:
        return redirect('profile', username=username)
    post = get_object_or_404(Post, author__username=username, id=post_id)
    form = PostForm(request.POST or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect('profile', username=username)

    return render(request, 'post.html', {'form': form})

def page_not_found(request, exception):
    # Переменная exception содержит отладочную информацию,
    # выводить её в шаблон пользователской страницы 404 мы не станем
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500)


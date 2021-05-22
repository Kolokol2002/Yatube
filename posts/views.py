from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from requests import request

from .forms import CommentForm, GroupForm, PostForm
from .models import Comment, Follow, Group, Post, User

from django.views.generic import (ListView,
                                  DetailView,
                                  CreateView,
                                  UpdateView,
                                  DeleteView)


class IndexListView(ListView):
    model = Post
    template_name = 'index.html'
    paginate_by = 5
    context_object_name = 'post_list'
    extra_context = {
        'index_page': True
    }


# def group_posts(request, slug):
#     '''Страница с публикиями связанными с группой'''
#     group = get_object_or_404(Group, slug=slug)
#     post_list = Post.objects.filter(
#         group=group).select_related(
#             'author', 'group').annotate(
#                 comment_count=Count(
#                     'commented_post')).order_by("-pub_date").all()
#     paginator = Paginator(post_list, 10)
#     page_number = request.GET.get('page')
#     page = paginator.get_page(page_number)
#     return render(request, "group.html", {'group': group,
#                                           'post_list': page,
#                                           'paginator': paginator})
class GroupPostView(ListView):
    model = Post
    template_name = 'group.html'
    paginate_by = 5
    context_object_name = 'post_list'

    @property
    def extra_context(self):
        return {
            'group': get_object_or_404(Group, slug=self.kwargs['slug'])
        }

    def get_queryset(self, *args, **kwargs):
        query_set = super().get_queryset()
        return query_set.filter(
        group__slug=self.kwargs['slug']).select_related(
            'author', 'group')


# @login_required
# def new_post(request):
#     '''Страница создания новой публикации'''
#     if request.method == 'POST':
#         form = PostForm(request.POST, files=request.FILES or None)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.save()
#             messages.add_message(
#                 request, messages.SUCCESS, f'Новая запись добавлена', extra_tags='success'
#             )
#             return redirect('index')
#     else:
#         form = PostForm()
#     return render(request, 'new_post.html', {'form': form})

# @login_required
class NewPostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'new_post.html'
    extra_context = {
        'title': 'Создать новою запись'
    }

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f'Новая запись добавлена'
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('index')


# def post_view(request, post_id, username):
#     '''Страница отдельной публикации'''
#     user_profile = get_object_or_404(
#         User.objects.filter(username=username).annotate(
#             follower_count=Count('follower', distinct=True),
#             following_count=Count('following', distinct=True),
#             post_count=Count('post_author', distinct=True)))
#     post = get_object_or_404(
#         Post.objects.annotate(
#             comment_count=Count(
#                 'commented_post')).select_related('author', 'group'),
#         pk=post_id)
#     post_comment = Comment.objects.filter(
#         post=post_id).select_related('author').order_by("-created").all()
#     form = CommentForm()
#     following = False
#     if request.user.is_authenticated:
#         if Follow.objects.filter(author=user_profile,
#            user=request.user).exists():
#             following = True
#     return render(request, 'post_view.html', {'post': post,
#                                               'profile': user_profile,
#                                               'comments': post_comment,
#                                               'form': form,
#                                               'following': following})
class PostView(ListView):
    model = Comment
    template_name = 'post_view.html'
    context_object_name = 'comments'

    @property
    def extra_context(self):
        user_profile = get_object_or_404(
            User.objects.filter(username=self.kwargs['username']).annotate(
                follower_count=Count('follower', distinct=True),
                following_count=Count('following', distinct=True),
                post_count=Count('post_author', distinct=True)))

        post = get_object_or_404(
            Post.objects.annotate(
                comment_count=Count(
                    'commented_post')).select_related('author', 'group'),
            pk=self.kwargs['post_id'])

        following = False
        if self.request.user.is_authenticated:
            if Follow.objects.filter(author=user_profile,
                                     user=self.request.user).exists():
                following = True
        return {'post': post,
                'profile': user_profile,
                'form': CommentForm(),
                'following': following}


    def get_queryset(self):
        query_set = super().get_queryset()
        return query_set.filter(
        post=self.kwargs['post_id']).select_related('author')


# def profile(request, username):
#     '''Страница с публикациями пользователя'''
#     user_profile = get_object_or_404(
#         User.objects.filter(
#             username=username).annotate(
#                 follower_count=Count('follower', distinct=True),
#                 following_count=Count('following', distinct=True)))
#     post_list = Post.objects.filter(
#         author=user_profile).select_related(
#             'group', 'author').annotate(
#                 comment_count=Count(
#                     'commented_post')).order_by("-pub_date").all()
#     paginator = Paginator(post_list, 10)
#     page_number = request.GET.get('page')
#     page = paginator.get_page(page_number)
#     following = False
#     if request.user.is_authenticated:
#         if Follow.objects.filter(author=user_profile,
#            user=request.user).exists():
#             following = True
#     return render(request, "profile.html", {'profile': user_profile,
#                                             'post_list': page,
#                                             'paginator': paginator,
#                                             'following': following})
class ProfileView(ListView):
    model = Post
    template_name = 'profile.html'
    paginate_by = 5
    context_object_name = 'post_list'

    @property
    def extra_context(self):
        profile = get_object_or_404(
            User.objects.filter(
                username=self.kwargs['username']).annotate(
                    follower_count=Count('follower', distinct=True),
                    following_count=Count('following', distinct=True)))

        following = False
        if self.request.user.is_authenticated:
            if Follow.objects.filter(author=profile,
                                     user=self.request.user).exists():
                following = True
        return {
            'profile': profile,
            'following': following
        }

    def get_queryset(self):
        profile = get_object_or_404(
            User.objects.filter(
                username=self.kwargs['username']).annotate(
                follower_count=Count('follower', distinct=True),
                following_count=Count('following', distinct=True)))
        query_set = super().get_queryset()
        return query_set.filter(
        author=profile).select_related(
            'group', 'author')


# @login_required
# def post_edit(request, username, post_id):
#     '''Страница редактирования публикации'''
#     title = 'Редактировать запись'
#     post = get_object_or_404(Post.objects.select_related('author'), pk=post_id)
#     if request.user == post.author:
#         if request.method == "POST":
#             form = PostForm(request.POST or None,
#                             files=request.FILES or None,
#                             instance=post)
#             if form.is_valid():
#                 post = form.save(commit=False)
#                 post.pub_date = timezone.now()
#                 post.save()
#                 return redirect('post', post_id=post.pk, username=username)
#         else:
#             form = PostForm(instance=post)
#     else:
#         return redirect('post', post_id=post.pk, username=post.author)
#     return render(
#         request, "new_post.html", {'form': form, 'title': title, 'post': post})
class PostEditUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    slug_field = 'username'
    pk_url_kwarg = 'post_id'
    form_class = PostForm
    template_name = 'new_post.html'
    extra_context = {
        'title': 'Редактировать запись'
    }

    def form_valid(self, form):
        post = form.save(commit=False)
        post.pub_date = timezone.now()
        post.save()
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f'Запись обновлена!',
            extra_tags='success'
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('profile', kwargs={
            'username': self.object.author,
        })

# @login_required
# def post_delete(request, username, post_id):
#     '''Функция для удаления публикации'''
#     post = get_object_or_404(Post, pk=post_id)
#     if request.user == post.author:
#         post.delete()
#         return redirect('profile', username=username)
#     return redirect('post', post_id=post.pk, username=post.author)
class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    slug_field = 'username'
    pk_url_kwarg = 'post_id'
    success_message = 'Запись удалена'



    def get_success_url(self):
        return reverse('profile', kwargs={
            'username': self.object.author,
        })


# @login_required
# def add_comment(request, username, post_id):
#     '''Функция для добавления комментария к публикации'''
#     post = get_object_or_404(Post, pk=post_id)
#     if request.method == 'POST':
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.post = post
#             comment.author = request.user
#             comment.save()
#             return redirect('post', post_id=post_id, username=username)
#     return redirect('post', post_id=post_id, username=username)
class AddCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    template_name = 'comments.html'
    form_class = CommentForm
    slug_field = 'username'
    pk_url_kwarg = 'post_id'

    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        comment = form.save(commit=False)
        comment.post = post
        comment.author = self.request.user
        comment.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post', kwargs={'username': self.object.author,
                                       'post_id': self.object.post.pk
                                       })


# @login_required
# def follow_index(request):
#     '''Страница с публикациями избранных пользователей'''
#     follow_page = True
#     post_list = Post.objects.filter(
#         author__following__user=request.user).select_related(
#             'group', 'author').annotate(
#                 comment_count=Count(
#                     'commented_post')).order_by("-pub_date").all()
#     paginator = Paginator(post_list, 10)
#     page_number = request.GET.get('page')
#     page = paginator.get_page(page_number)
#     return render(request, "follow.html", {'page': page,
#                                            'paginator': paginator,
#                                            'follow_page': follow_page})
class FollowIndexView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'follow.html'
    paginate_by = 5
    context_object_name = 'post_list'
    extra_context = {
        'follow_page': True
    }

    def get_queryset(self):
        query_set = super().get_queryset()
        return query_set.filter(
        author__following__user=self.request.user).select_related(
            'group', 'author')


@login_required
def profile_follow(request, username):
    '''Функция для подписки на пользователя'''
    followed_author = get_object_or_404(User, username=username)
    if followed_author == request.user:
        return redirect('profile', username=username)
    if Follow.objects.filter(user=request.user,
                             author=followed_author).exists():
        return redirect('profile', username=username)
    Follow.objects.create(author=followed_author, user=request.user)
    return redirect('profile', username=username)


@login_required
def profile_unfollow(request, username):
    '''Функция для отписки от пользователя'''
    follover = Follow.objects.filter(author__username=username,
                                     user=request.user)
    follover.delete()
    return redirect('profile', username=username)


@login_required
def delete_comment(request, username, post_id, comment_id):
    '''Функция для удаления комментария к публикации'''
    comment = get_object_or_404(Comment, post=post_id, pk=comment_id)
    if request.user == comment.author:
        comment.delete()
    return redirect('post', username=username, post_id=post_id)


# @login_required
# def edit_comment(request, username, post_id, comment_id):
#     '''Функция для редактирования комментария к публикации'''
#     title = 'Редактировать комментарий'
#     comment = get_object_or_404(Comment, post=post_id, pk=comment_id)
#     if request.user == comment.author:
#         if request.method == 'POST':
#             form = CommentForm(request.POST, instance=comment)
#             if form.is_valid():
#                 comment = form.save(commit=False)
#                 comment.created = timezone.now()
#                 comment.save()
#                 return redirect('post', username=username, post_id=post_id)
#         form = CommentForm(instance=comment)
#     return render(request, "new_post.html", {'form': form, 'title': title})
class CommentEditView(LoginRequiredMixin, UpdateView):
    model = Comment
    template_name = 'new_post.html'
    form_class = CommentForm
    pk_url_kwarg =  'comment_id'
    extra_context = {
        'title': 'Редактировать комментарий'
    }

    def form_valid(self, form):
        comment = form.save(commit=False)
        comment.created = timezone.now()
        comment.save()
        messages.add_message(
            self.request,
            messages.SUCCESS,
            f'Коментарий отредактирован',
        )
        return super().form_valid(form)


    def get_success_url(self):
        return reverse('post', kwargs={'username': self.object.author,
                                       'post_id': self.object.post.pk
                                       })


# @login_required
# def add_group(request):
#     '''Страница для добавления группы'''
#     title = 'Создать группу'
#     if request.method == 'POST':
#         form = GroupForm(request.POST)
#         if form.is_valid():
#             slug = form.cleaned_data['slug']
#             form.save()
#             return redirect("group", slug=slug)
#         return render(request, "new_post.html", {'form': form, 'title': title})
#     form = GroupForm()
#     return render(request, "new_post.html", {'form': form, 'title': title})
class GroupAddView(LoginRequiredMixin, CreateView):
    model = Group
    template_name = 'new_post.html'
    form_class = GroupForm
    extra_context = {
        'title': 'Создать группу'
    }

    def get_success_url(self, **kwargs):
        return reverse('group', kwargs={'slug': self.object.slug})



def page_not_found(request, exception):
    '''Страница 404'''
    return render(request, "misc/404.html", {"path": request.path}, status=404)


def server_error(request):
    '''Страница 500'''
    return render(request, "misc/500.html", status=500)
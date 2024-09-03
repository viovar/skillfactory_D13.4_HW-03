from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group, User

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.cache import cache

from django.db import models
from django.db.models import Exists, OuterRef
from django.db.models import Q

from django.shortcuts import render, get_object_or_404, redirect

from django.views.decorators.csrf import csrf_protect
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)

from django.urls import reverse_lazy

from .import models
from .filters import PostFilter
from .forms import PostForm, ArticleForm, BasicSignupForm
from .models import Subscription, Category, Post

from .tasks import send_notification_to_subscribers, send_weekly_newsletter


# Create your views here.

class PostList(ListView):
    model = Post
    ordering = 'dateCreation'
    template_name = 'flatpages/news.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by(
        '-dateCreation'
    )
    paginate_by=2

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class NewDetail(DetailView):
    model = Post
    template_name = 'flatpages/new.html'
    context_object_name = 'post'

    def get_object(self, *args, **kwargs):  # переопределяем метод получения объекта
        obj = cache.get(f'news-{self.kwargs["pk"]}', None)

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'news-{self.kwargs["pk"]}', obj)
            return obj


class PostSearch(ListView):
    model = Post
    ordering = 'dateCreation'
    template_name = 'post_search.html'
    context_object_name = 'search'
    paginate_by = 4

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset']=self.filterset
        return context


class PostCreate(LoginRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'create_news.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == '/news/create/':
            post.categoryType = 'NW'
        post.save()
        complete_post.apply_async([post.pk], countdown=60)
        # return redirect('/')
        return super().form_valid(form)


class PostUpdate(UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    fields = ['title', 'text', 'categories']

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == '/news/<int:pk>/edit/':
            post.categoryType = 'NW'
        post.save()
        return super().form_valid(form)


class PostDelete(DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list') #This redirects to the home page after deleting a post

    def get_template_names(self):
        post = self.get_object()
        if post.categoryType == 'AR':
            return ['articles_delete.html']
        elif post.categoryType == 'NW':
            return ['post_delete.html']
        else:
            pass

    # def delete(self, request, *args, **kwargs):
    #     """
    #     Overridden method to perform the deletion of the post.
    #     """
    #     self.object = self.get_object()
    #     success_url = self.get_success_url()
    #     self.object.delete()
    #     return HttpResponseRedirect(success_url)

class CategoryListView(ListView):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(postCategory=self.category).order_by('-dateCreation')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context

@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )


# class IndexView(View):
#     def get(self, request):
#         printer.apply_async([10],
#                            eta = datetime.now() + timedelta(seconds=5))
#         hello.delay()
#         return HttpResponse('Hello!')

# class IndexView(TemplateView):
#     template_name = "index.html"
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['post'] = Post.objects.all()
#         return context
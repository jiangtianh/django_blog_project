from typing import Any, Dict
from django.db import models
from django.shortcuts import render


# Create your views here.
# def home(request):
#     return render(request, 'home.html', {})


from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from .models import Post, Category, Comment
from .forms import PostForm, EditPostForm, AddCategoryForm, CommentForm
from django.urls import reverse_lazy, reverse
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect
from django.http import Http404, HttpResponseRedirect

class HomeView(ListView):
    model = Post 
    template_name = 'home.html'
    context_object_name = 'all_posts_list'
    ordering = ['-post_created_date', '-pk']

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(HomeView, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu

        return context


class ArticleDetailView(DetailView):
    model = Post
    template_name = 'article_details.html'
    context_object_name = 'post'

    def get_context_data(self, *args, **kwargs):
        cat_menu = Category.objects.all()
        context = super(ArticleDetailView, self).get_context_data(*args, **kwargs)
        context["cat_menu"] = cat_menu

        post = get_object_or_404(Post, id=self.kwargs['pk'])
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True
        else:
            liked = False
        context["liked"] = liked
        context["form"] = CommentForm()

        return context
    
    def post(self, request, *args, **kwargs):
        post = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = get_object_or_404(Post, id=self.kwargs['pk'])
            new_comment.user = self.request.user
            new_comment.save()
        return self.get(request, *args, **kwargs)


class AddPostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'add_post.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


    
class AddCategoryView(CreateView):
    model = Category
    template_name = 'add_category.html'
    form_class = AddCategoryForm

    def form_valid(self, form):
        try:
            form.instance.name = modify_category_name(form.cleaned_data['name'])
            return super().form_valid(form)
        except IntegrityError:
            error_message = 'Category with this name already exists.'
            context = self.get_context_data(form=form, error_message=error_message)
            return self.render_to_response(context)
    
def modify_category_name(name):
    name = name.split(' ')
    name = [word.capitalize() for word in name]
    name = ' '.join(name)
    return name

class UpdatePostView(UpdateView):
    model = Post
    template_name = 'update_post.html'
    form_class = EditPostForm

class DeletePostView(DeleteView):
    model = Post 
    template_name = 'delete_post.html'
    success_url = reverse_lazy('home')

def CategoryView(request, categ):
    try:
        category = get_object_or_404(Category, name=categ)
        category_posts = Post.objects.filter(category=category)
    except Category.DoesNotExist:
        raise Http404("Category does not exist")
    return render(request, 'categories.html', {'categ': category.name, 'category_posts': category_posts})

def CategoryListView(request):
    cat_menu_list = Category.objects.all()
    return render(request, 'category_list.html', {'cat_menu_list': cat_menu_list})


def LikeView(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))

    liked = False 
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
        
    return HttpResponseRedirect(reverse('article_details', args=[pk,]))

def DeleteCommentView(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    
    # Check if the user is the author of the comment
    if request.user == comment.user:
        comment.delete()
    
    return redirect('article_details', pk=comment.post.pk)








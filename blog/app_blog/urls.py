from django.urls import path

from .views import HomeView, ArticleDetailView, AddPostView, UpdatePostView, DeletePostView, AddCategoryView, CategoryView, CategoryListView, LikeView, DeleteCommentView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('article/<int:pk>/', ArticleDetailView.as_view(), name='article_details'),
    path('create_post/', AddPostView.as_view(), name='create_post'),
    path('article/<int:pk>/edit/', UpdatePostView.as_view(), name='update_post'), 
    path('article/<int:pk>/delete/', DeletePostView.as_view(), name='delete_post'),  
    #path('<slug:author>/', ArticleDetailByAuthorView.as_view(), name='by_author'),

    path('add_category/', AddCategoryView.as_view(), name='add_category'),  

    path('category/<str:categ>/', CategoryView, name='category'),
    path('category-list/', CategoryListView, name='category-list'),

    path('like/<int:pk>/', LikeView, name='like_post'),

    path('delete_comment/<int:comment_id>/', DeleteCommentView, name='delete_comment'),
]
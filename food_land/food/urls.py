from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings


from . import views
# from .views import HomePage

urlpatterns = [
    path('trending/', views.TrendingRecipes.as_view(), name='trending'),
    path('category/', views.CategoryListAndDetailsView.as_view(), name='category'),
    path('category/<int:pk>/', views.CategoryListAndDetailsView.as_view(), name='category_details'),
    path('recipes/', views.RecipeListAndDetailsView.as_view(), name='recipes'),
    path('recipes/<int:pk>/', views.RecipeListAndDetailsView.as_view(), name='recipes_details'),
    path('blogs/', views.BlogListAndDetailsView.as_view(), name='blog'),
    path('blogs/<int:pk>/', views.BlogListAndDetailsView.as_view(), name='blog_details'),
    path('contact_us/', views.Contact.as_view(), name='contact_us'),
    path('about_us/',views.About.as_view(), name='about_us'),
    path('subscribe/', views.SubscribeView.as_view(), name='subscribe'),
    path('search_blog/', views.SearchBlogs.as_view(), name='search'),
    path('like/<int:pk>/', views.LikeRecipe.as_view(), name='like'),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

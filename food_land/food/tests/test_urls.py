import pytest
from django.test import Client
from django.urls import reverse, resolve

from food.views import *


@pytest.mark.django_db
def test_trending_url():
    path = reverse("trending")
    match = resolve(path)
    assert match.url_name == "trending"
    assert match.func.view_class == TrendingRecipes


    # client = Client()
    #
    # url = reverse('trending')
    # response = client.get(url)
    # assert response.status_code == 200
    
@pytest.mark.django_db
def test_category_url():
    path = reverse('category')
    match = resolve(path)
    assert match.url_name == 'category'
    assert match.func.view_class == CategoryListAndDetailsView

@pytest.mark.django_db
def test_category_detail_url():
    path=reverse('category_details', kwargs={'pk':1})
    match = resolve(path)
    assert match.url_name == 'category_details'
    assert match.func.view_class == CategoryListAndDetailsView

@pytest.mark.django_db
def test_recipes_url():
    path = reverse('recipes')
    match = resolve(path)
    assert match.url_name == 'recipes'
    assert match.func.view_class == RecipeListAndDetailsView

@pytest.mark.django_db
def test_recipe_detail_url():
    path = reverse('recipes_details', kwargs={'pk':1})
    match = resolve(path)
    assert match.url_name == 'recipes_details'
    assert match.func.view_class == RecipeListAndDetailsView

@pytest.mark.django_db
def test_blog_url():
    path = reverse('blog')
    match = resolve(path)
    assert match.url_name == 'blog'
    assert match.func.view_class == BlogListAndDetailsView

@pytest.mark.django_db
def test_blog_detail_url():
    path = reverse('blog_details', kwargs={'pk':1})
    match = resolve(path)
    assert match.url_name == 'blog_details'
    assert match.func.view_class == BlogListAndDetailsView

@pytest.mark.django_db
def test_contactus_url():
    path = reverse("contact_us")
    match = resolve(path)
    assert match.url_name == 'contact_us'
    assert match.func.view_class == Contact


@pytest.mark.django_db
def test_about_us_url():
    path = reverse('about_us')
    match = resolve(path)
    assert match.url_name == 'about_us'
    assert match.func.view_class == About

@pytest.mark.django_db
def test_subscribe_url():
    path = reverse('subscribe')
    match = resolve(path)
    assert match.url_name == 'subscribe'
    assert match.func.view_class == Subscribe

@pytest.mark.django_db
def test_search_blog_url():
    path = reverse('search')
    match = resolve(path)
    assert match.url_name == 'search'
    assert match.func.view_class == SearchBlogs


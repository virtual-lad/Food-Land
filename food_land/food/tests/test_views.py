from pyexpat.errors import messages

import pytest
from datetime import timedelta, timezone, datetime
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User

from food.models import *
from food.views import LikeRecipe


@pytest.mark.django_db
class TestCategoryView:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = APIClient()
        self.obj1 = Category.objects.create(name="test1")
        self.obj2 = Category.objects.create(name="test2")
        self.sub_obj3 = SubCategory.objects.create(name="subtest1", category=self.obj1)

    @pytest.fixture(autouse=True)
    def cleanup(self, request):
        def delete_objects():
            self.obj1.delete()
            self.obj2.delete()
            self.sub_obj3.delete()

        request.addfinalizer(delete_objects)

    def test_category_view(self):
        url = reverse("category")
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        assert response.data[0]['name'] == "test1"

    def test_category_detail_view(self):
        url = reverse("category_details", kwargs={'pk' : self.obj1.pk})
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        sub = response.data['sub']
        assert sub[0]['name'] == 'subtest1'

@pytest.mark.django_db
class TestRecipeView:

    @pytest.fixture(autouse=True)
    def setup_method(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuserinfinity', password='testpassword')
        self.author = Author.objects.create(name='author')
        self.main_ing = MainDish.objects.create(name='main_dish')
        self.sauce_ing = Sauce.objects.create(name='sauce')
        self.category = Category.objects.create(name='category')
        self.subcategory = SubCategory.objects.create(name='subcategory', category=self.category)
        self.recipe = Recipe.objects.create(
            title = 'recipe',
            author = self.author,
            category = self.subcategory,
            description = 'test description',
            direction = 'test direction',
            prep_time = timedelta(minutes=30),
            cook_time = timedelta(minutes=40),
            most_liked = 10,
            hand_pick = False
        )
        self.recipe.main_ing.add(self.main_ing)
        self.recipe.sauce_ing.add(self.sauce_ing)
        self.client.force_authenticate(user=self.user)

    @pytest.fixture(autouse=True)
    def cleanup(self, request):
        def delete_objects():
            self.recipe.delete()
            self.author.delete()
            self.user.delete()
            self.main_ing.delete()
            self.sauce_ing.delete()
            self.category.delete()
            self.subcategory.delete()

        request.addfinalizer(delete_objects)

    @pytest.mark.django_db
    def test_recipe_list(self):
        url = reverse('recipes')
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['title'] == 'recipe'

    @pytest.mark.django_db
    def test_recipe_detail(self):
        url = reverse('recipes_details', kwargs={'pk' : self.recipe.id})
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['recipe']['title'] == 'recipe'             # {'nutrition':[], 'recipe':{'fields'.....}}
        assert response.data['recipe']['description'] == 'test description'
        assert response.data['recipe']['direction'] == 'test direction'

@pytest.mark.django_db
class TestBlogView:

    @pytest.fixture(autouse=True)
    def setup_method(self):
        self.client = APIClient()
        self.author1 = Author.objects.create(name='author1')
        self.author2 = Author.objects.create(name='author2')
        self.blog1 = Blog.objects.create(
            title = 'blog1',
            description = 'test 1 description',
            author = self.author1,
            date = datetime(2024, 5, 17).date(),
            body = 'test 1 body',
        )
        self.blog2 = Blog.objects.create(
            title = 'blog2',
            description = 'test 2 description',
            author = self.author2,
            date = datetime(2024, 5, 17).date(),
            body = 'test 2 body',
        )

    @pytest.fixture(autouse=True)
    def cleanup(self, request):
        def delete_objects():
            self.blog1.delete()
            self.author1.delete()
            self.blog2.delete()
            self.author2.delete()

        request.addfinalizer(delete_objects)

    def test_blog_list(self):
        url = reverse('blog')
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2
        assert response.data[0]['title'] == 'blog1'
        assert response.data[1]['title'] == 'blog2'

    def test_blog_detail(self):
        url = reverse("blog_details", kwargs={'pk' : self.blog1.id})
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 7
        assert response.data['description'] == 'test 1 description'
        assert response.data['title'] == 'blog1'

@pytest.mark.django_db
class TestContactView:

    @pytest.fixture(autouse=True)
    def setup_method(self):
        self.client = APIClient()

    @pytest.fixture(autouse=True)
    def cleanup(self, request):
        def delete_objects():
            ContactUs.objects.filter().first().delete()

        request.addfinalizer(delete_objects)

    @pytest.mark.django_db
    def test_contact_view(self):
        url = reverse('contact_us')
        data={
            'name' : 'faisal',
            'email' : '123@gmail.com',
            'subject' : 'Test Subject',
            'enquiry_type' : 'obj1',
            'message' : 'Test Message'
        }
        response = self.client.post(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert ContactUs.objects.count() == 1
        contact = ContactUs.objects.first()
        assert contact.name == 'faisal'
        assert contact.email == '123@gmail.com'

@pytest.mark.django_db
class TestAboutUsView:

    @pytest.fixture(autouse=True)
    def setup_method(self):
        self.client = APIClient()
        self.about1 = AboutUs.objects.create(resturant_name='about1', body='Test 1 Body Of About Us')
        self.about2 = AboutUs.objects.create(resturant_name='about2', body='Test 2 Body Of About Us')
        self.about3 = AboutUs.objects.create(resturant_name='about3', body='Test 3 Body Of About Us')

    @pytest.fixture(autouse=True)
    def cleanup(self, request):
        def delete_objects():
            self.about1.delete()
            self.about2.delete()
            self.about3.delete()

        request.addfinalizer(delete_objects)

    def test_about_view(self):
        url = reverse('about_us')
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3
        assert response.data[0]['body'] == 'Test 1 Body Of About Us'
        assert response.data[1]['body'] == 'Test 2 Body Of About Us'

@pytest.mark.django_db
class TestSubscribeView:

    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = APIClient()

    @pytest.fixture(autouse=True)
    def cleanup(self, request):
        def delete_objects():
            Subscribe.objects.all().delete()

        request.addfinalizer(delete_objects)

    def test_subscribe(self):
        url = reverse('subscribe')
        data = {
            'email' : 'test123@gmail.com',
        }
        response = self.client.post(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert Subscribe.objects.count() == 1
        update = Subscribe.objects.first()
        assert update.email == 'test123@gmail.com'

    def test_subscribe_with_same_email(self):
        Subscribe.objects.create(email='test123@gmail.com')

        url = reverse('subscribe')
        data = {
            'email' : 'test123@gmail.com',
        }

        data = {
            'email' : 'test123@gmail.com',
        }
        response = self.client.post(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert Subscribe.objects.count() == 1
        assert response.data['message'] == 'Email already exists'

    def test_subscribe_without_email(self):
        url = reverse('subscribe')
        data = {
            'email' : '',
        }
        response = self.client.post(url, data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert Subscribe.objects.count() == 0
        assert response.data['email'][0] == 'This field may not be blank.'



@pytest.mark.django_db
class TestLikeRecipe:

    @pytest.fixture(autouse=True)
    def set_up(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='blahblah', password='blahtestpassword')
        self.author = Author.objects.create(name='blah_author')
        self.main = MainDish.objects.create(name='main_dish_object')
        self.sauce = Sauce.objects.create(name='sauce_object')
        self.category = Category.objects.create(name='blah_category')
        self.sub = SubCategory.objects.create(name='blah_subcategory', category=self.category)
        self.recipe = Recipe.objects.create(
            title='blah_recipe',
            author=self.author,
            category=self.sub,
            description='blah test description',
            direction='blah test direction',
            prep_time=timedelta(minutes=20),
            cook_time=timedelta(minutes=40),
            most_liked=0,
            hand_pick=False
        )
        self.recipe.main_ing.add(self.main)
        self.recipe.sauce_ing.add(self.sauce)
        self.client.force_authenticate(user=self.user)

    @pytest.fixture(autouse=True)
    def cleanup(self, request):
        def delete_obj():
            self.recipe.delete()
            self.author.delete()
            self.user.delete()
            self.main.delete()
            self.sauce.delete()
            self.category.delete()
            self.sub.delete()

        request.addfinalizer(delete_obj)

    def test_like_recipe(self):
        # Test liking a recipe
        url = reverse('like', kwargs={'pk' : self.recipe.id})
        response = self.client.post(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['message'] == 'Successfully liked this recipe!'
        rec = Recipe.objects.first()
        assert rec.most_liked == 1
        assert Like.objects.filter(recipe=self.recipe, user=self.user).exists()

        # Test disliking a recipe
    def test_dislike_recipe(self):
        Like.objects.create(recipe=self.recipe, user=self.user)
        self.recipe.most_liked = 1
        self.recipe.save()

        url = reverse('like', kwargs={'pk' : self.recipe.id})
        response = self.client.post(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['message'] == 'Successfully disliked this recipe!'
        rec = Recipe.objects.first()
        assert rec.most_liked == 0
        assert not Like.objects.filter(recipe=self.recipe, user=self.user).exists()

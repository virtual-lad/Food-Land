from django.contrib.auth.models import User
from django.db.models import OuterRef, Exists
from rest_framework import serializers
from .models import Recipe, Category, Blog, ContactUs, SubCategory, RecipeNutrition, AboutUs, Like, Subscribe


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['name']

class PreviewRecipeSerializer(serializers.ModelSerializer):
    is_liked = serializers.BooleanField()

    class Meta:
        model = Recipe
        fields = ['title', 'image', 'category', 'duration', 'is_liked']

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = "__all__"

class RecipeNutritionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeNutrition
        fields = "__all__"

class PreviewBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model= Blog
        fields=['title', 'description', 'author', 'date', 'image']

class  BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = "__all__"

class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = "__all__"

class UpdatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscribe
        fields = ['email']

class AboutUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUs
        fields = ['body']

class TrendingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ['title', 'author', 'description', 'image', 'duration']
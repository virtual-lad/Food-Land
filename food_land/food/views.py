from django.db.models import OuterRef, Exists
from rest_framework import status
from rest_framework.generics import ListAPIView, get_object_or_404, GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import *
from .serializer import *


# @api_view(['GET'])
# def trending(request):
#     trend = Recipe.objects.order_by('-most_liked')[:5]
#     recipe_serializer = TrendingSerializer(trend, many=True)
#
#     return Response(recipe_serializer.data)

class TrendingRecipes(ListAPIView):
    authentication_classes = []
    permission_classes = []
    model = Recipe
    serializer_class = TrendingSerializer
    queryset = Recipe.objects.order_by('-most_liked')[:5]

# @api_view(['GET'])
# def category(request):                                                         # All Categories
#     categories = Category.objects.all()
#     category_serializer = CategorySerializer(categories, many=True)
#     return Response(category_serializer.data)

# @api_view(['GET'])
# def category_details(request,pk):                                               # Category Details
#     cat_details = Category.objects.get(pk=pk)
#     sub_categories = SubCategory.objects.filter(category=cat_details)
#     sub_serializer = SubCategorySerializer(sub_categories, many=True)
#     return Response(sub_serializer.data)

class CategoryListAndDetailsView(GenericAPIView, ListModelMixin):
    authentication_classes = []
    permission_classes = []
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            cat_details = get_object_or_404(Category, pk=pk)
            sub_categories = SubCategory.objects.filter(category=cat_details)
            cat_serializer = self.serializer_class(cat_details, many=False)
            sub_serializer = SubCategorySerializer(sub_categories, many=True)

            context={
                'cat' : cat_serializer.data,
                'sub': sub_serializer.data,
            }

            return Response(context)
        else:
            return self.list(request, *args, **kwargs)

# @api_view(["GET"])
# def recipes_view(request):
#     recipe = Recipe.objects.all()                                                # All Recipes
#     recipe_serializer = RecipeSerializer(recipe, many=True)
#     return Response(recipe_serializer.data)

class RecipeListAndDetailsView(GenericAPIView, ListModelMixin):
    queryset = Recipe.objects.all()
    serializer_class = PreviewRecipeSerializer

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            recipe_details = get_object_or_404(Recipe, pk=pk)
            nutrition = RecipeNutrition.objects.filter(recipe=pk)  # Recipe Nutrients
            nutrition_serializer = RecipeNutritionSerializer(nutrition, many=True)
            recipe_detail_serializer = RecipeSerializer(recipe_details, many=False)
            context={
                'nutrition' : nutrition_serializer.data,
                'recipe' : recipe_detail_serializer.data,
            }
            return Response(context)
        else:
            user = request.user
            subquery = Like.objects.filter(user=user, recipe=OuterRef('pk'))
            queryset = Recipe.objects.annotate(is_liked=Exists(subquery))
            serializer = self.serializer_class(queryset, many=True)
            return Response(serializer.data)

# @api_view(["GET"])
# def recipe_details(request, pk):                                                 # Recipe Details 404
#     recipe_id = Recipe.objects.get(pk=pk)
#     nutrition = RecipeNutrition.objects.filter(recipe=recipe_id)                 # Recipe Nutrients
#     nutrition_serializer = RecipeNutritionSerializer(nutrition, many=True)
#     detail_serializer = RecipeSerializer(recipe_id, many=False)
#
#     context = {
#         'detail' : detail_serializer.data,
#         'nutrition' :nutrition_serializer.data,
#     }
#     return Response(context)

# @api_view(['GET'])
# def blog(request):                                                                # All Blogs
#     blogs = Blog.objects.all()
#     blog_serializer = BlogSerializer(blogs, many=True)
#
#     return Response(blog_serializer.data)

# @api_view(["Get"])
# def blog_detail(request, pk):                                                      # Blog Details 404
#     blog_id = Blog.objects.get(pk=pk)
#     detail_serializer = BlogSerializer(blog_id, many=False)
#
#     return Response(detail_serializer.data)

class BlogListAndDetailsView(GenericAPIView, ListModelMixin):
    authentication_classes = []
    permission_classes = []
    queryset = Blog.objects.all()
    serializer_class = PreviewBlogSerializer

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk:
            blog_details = get_object_or_404(Blog, pk=pk)
            blog_serializer = BlogSerializer(blog_details, many=False)
            return Response(blog_serializer.data)
        else:
            return self.list(request, *args, **kwargs)

# @api_view(["POST"])
# def contact_us(request):                                                           # Contact Us Form/Page
#     contact_serializer = ContactUsSerializer(data=request.data)
#     if contact_serializer.is_valid():
#
#         ContactUs.objects.create(**contact_serializer.data)
#         return Response({'message':'Success'})
#
#     return Response(contact_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Contact(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        contact_serializer = ContactUsSerializer(data=request.data)
        if contact_serializer.is_valid():
            ContactUs.objects.create(**contact_serializer.data)
            return Response({'message':'Success'})

        return Response(contact_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(["GET"])
# def about_us(request):                                                              # About Us
#     about_data = AboutUs.objects.all()
#     about_serializer = AboutUsSerializer(about_data, many=True)
#     return Response(about_serializer.data)

class About(ListAPIView):
    authentication_classes = []
    permission_classes = []

    queryset = AboutUs.objects.all()
    serializer_class = AboutUsSerializer
# @api_view(["POST"])
# def subscribe(request):
#     update_serializer = UpdatesSerializer(data=request.data, many=True)
#     if update_serializer.is_valid():
#         user = request.user
#         user.email = update_serializer.validated_data['email']
#         user.save()
#         return Response({'message': 'Success'})
#     return Response(update_serializer.errors)

class SubscribeView(APIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = UpdatesSerializer
    queryset = Subscribe.objects.all()

    def post(self, request):
        update_serializer = self.serializer_class(data=request.data, many=False)

        if update_serializer.is_valid():
            check = self.queryset.filter(**update_serializer.validated_data).first()
            if check:
                return Response({'message' : 'Email already exists'})
            else:
                self.queryset.create(**update_serializer.data)
                return Response({'message': 'success'})
        else:
            return Response(update_serializer.errors)

# @api_view(['GET'])
# def search_blog(request):                                                           # Search Blogs
#     search = request.GET.get('search')
#     if search:
#         blogs = Blog.objects.filter(title__icontains=search)
#         serializer = BlogSerializer(blogs, many=True)
#         return Response(serializer.data)
#     else:
#         return Response({'message': 'Search term is required!'})

class SearchBlogs(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        search = request.GET.get('search')
        if search:
            blogs = Blog.objects.filter(title__icontains=search)
            serializer = BlogSerializer(blogs, many=True)
            return Response(serializer.data)
        else:
            return Response ({ 'message' : 'Search not found' })

class LikeRecipe(APIView):

    def post(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        like , created = Like.objects.get_or_create(recipe=recipe, user=request.user)
        if created:
            like.save()
            recipe.most_liked += 1
            recipe.save()
            return Response({'message': 'Successfully liked this recipe!'})
        else:
            like.delete()
            recipe.most_liked -= 1
            recipe.save()
        return Response({ 'message' : 'Successfully disliked this recipe!' })

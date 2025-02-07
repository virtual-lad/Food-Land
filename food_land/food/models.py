from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models
from django.db.models import ImageField
from django_ckeditor_5.fields import CKEditor5Field


class Category(models.Model):
    image = models.ImageField(upload_to="images/", null=True, blank=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Categories"

class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="sub_categories")

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Sub Categories"

class MainDish(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Main Dish Ingredient"
class Sauce(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Sauce Ingredient"

class Nutrition(models.Model):
    name = models.CharField(max_length=200,blank=True,null=True)
    unit = models.CharField(max_length=10,blank=True,null=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'Nutrition'

class Author(models.Model):
    name = models.CharField(max_length=100)
    image = ImageField(upload_to='images/', blank=True,null=True)

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Authors"

class Recipe(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    main_ing = models.ManyToManyField(MainDish, verbose_name='For Main Dish Ingredient')
    sauce_ing = models.ManyToManyField(Sauce, verbose_name='For Sauce Ingredient')
    category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    description = models.TextField()
    direction = CKEditor5Field()
    image = models.ImageField(upload_to='images/', null=True, blank=True)               # Change ImageField to FileField
    prep_time = models.DurationField(default=timedelta(minutes=0), verbose_name='Prep Time (In Minutes)')
    cook_time = models.DurationField(default=timedelta(minutes=0), verbose_name='Prep Time (In Minutes)')
    most_liked = models.IntegerField(default=0)
    hand_pick = models.BooleanField(default=False)


    @property
    def duration(self):
        total = (self.prep_time + self.cook_time).total_seconds()
        return int( total / 60)

    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural = "Recipes"

class RecipeNutrition(models.Model):
    recipe = models.ForeignKey(Recipe, related_name='nutrition', on_delete=models.CASCADE)
    nutrition = models.ForeignKey(Nutrition, on_delete=models.CASCADE)
    value = models.FloatField()

    def __str__(self):
        return f"{self.recipe.title} - {self.nutrition.name}: {self.value}{self.nutrition.unit}"

class Blog(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    description = models.TextField()
    date = models.DateField()
    body = CKEditor5Field()
    image = models.ImageField(upload_to="images/", null=True, blank=True)

    def __str__(self):
        return self.title
    class Meta:
        verbose_name_plural = "Blogs"

class ContactUs(models.Model):
    ChoiceList = [
        ("obj1", "Object 1"),
        ("obj2", "Object 2"),
        ("obj3", "Object 3"),
        ("obj4", "Object 4")
    ]
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    enquiry_type = models.CharField(max_length=4, choices=ChoiceList, default="obj1")
    message = models.TextField()

    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Contact Us"

class AboutUs(models.Model):
    resturant_name = models.CharField(max_length=100)
    body = CKEditor5Field()
    def __str__(self):
        return self.resturant_name
    class Meta:
        verbose_name_plural = "About Us"

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    class Meta:
        unique_together = ("user", "recipe")

    def __str__(self):
        return f"{self.user.username} - {self.recipe.title}"

class Subscribe(models.Model):
    email = models.EmailField()

    def __str__(self):
        return self.email


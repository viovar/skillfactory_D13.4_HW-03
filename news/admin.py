
from django.contrib import admin
from .models import Author, Comment, Post, Category, PostCategory


# Register your models here.
admin.site.register(Author)
admin.site.register(Comment)
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(PostCategory)
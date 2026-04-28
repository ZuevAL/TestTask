from django.contrib import admin
from . import models


@admin.register(models.Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'surname', 'email']


@admin.register(models.Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner']


@admin.register(models.AccessRule)
class AccessRoleAdmin(admin.ModelAdmin):
    list_display = ['role', 'element_name']
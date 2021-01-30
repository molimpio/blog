from django.contrib import admin
from .models import Post

"""
Quando adicionar o modelo no admin ele fica disponivel na interface 
do admin permitindo operacoes nos dados, CRUD

Abaixo eh mostrado como pode personalizar os campos no admin
"""


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')

from django.contrib import admin

# Register your models here.
from .models import Question
# Pollアプリをadmin上で編集できるようにする
admin.site.register(Question)
from django.contrib import admin
from .models import WordsFalse, PhrasesFalse, Student
# Register your models here.
admin.site.register(Student)
admin.site.register(WordsFalse)
admin.site.register(PhrasesFalse)
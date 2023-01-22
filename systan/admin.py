from django.contrib import admin
from .models import Words, Phrases, WordsFalse, PhrasesFalse, Student
# Register your models here.
admin.site.register(Student)
admin.site.register(Words)
admin.site.register(Phrases)
admin.site.register(WordsFalse)
admin.site.register(PhrasesFalse)
from django.db import models

# Create your models here.
class Words(models.Model):
    japanese = models.TextField()
    english = models.TextField()

class Phrases(models.Model):
    japanese = models.TextField()
    english = models.TextField()

class Student(models.Model):
    latest_login = models.DateTimeField(auto_now=True, null=True)

class WordsFalse(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    words = models.ForeignKey(Words, on_delete=models.CASCADE)

class PhrasesFalse(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    phrases = models.ForeignKey(Phrases, on_delete=models.CASCADE)
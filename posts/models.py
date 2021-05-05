from django.db import models
from django.contrib.auth import get_user_model
from django.forms import ModelForm
from django.views.generic import CreateView

class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self):
        return self.title

User = get_user_model()

class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name="group", blank=True, null=True
    )
    # image = models.ImageField(upload_to='posts/', blank=True, null=True)

    def __str__(self):
        return str(self.text)








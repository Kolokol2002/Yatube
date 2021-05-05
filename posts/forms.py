from django import forms
from django.forms import ModelForm, Textarea, CharField

from posts.models import Post




#  создадим собственный класс для формы регистрации
#  сделаем его наследником предустановленного класса UserCreationForm
class PostForm(ModelForm):
    class Meta:
        # укажем модель, с которой связана создаваемая форма
        model = Post
        # укажем, какие поля должны быть видны в форме и в каком порядке
        fields = ('text', 'group')

        widgets = {
            'text': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Текс к новой записи'
            }),

        }


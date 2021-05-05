#  импортируем CreateView, чтобы создать ему наследника

from django.views.generic import CreateView
import datetime as dt
from django.shortcuts import redirect, render

#  функция reverse_lazy позволяет получить URL по параметру "name" функции path()
#  берём, тоже пригодится
from django.urls import reverse_lazy

#  импортируем класс формы, чтобы сослаться на неё во view-классе
from .forms import CreationForm, ContactForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy("login") #  где login — это параметр "name" в path()
    template_name = "signup.html"


def year(request):
    """
    Добавляет переменную с текущим годом.
    """
    year = dt.date.today().year
    return {"year": year}

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, UpdateView
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login

from interface.forms import UserRegisterForm, UserUpdateForm, SmsCodeForm
from users.models import User
from users.services import generate_invite_code, create_unique_invite_code, send, generate_sms_code


class UserCreateView(CreateView):
    """Сохранение пользователя при первом входе, отправка кода для входа, присваивание invite_code при первом входе"""
    template_name = 'interface/register.html'
    model = User
    form_class = UserRegisterForm  # Форма для регистрации пользователя
    success_url = reverse_lazy('interface:login')  # URL для перенаправления при успешной регистрации

    def get_success_url(self):
        # Формируем URL для работы с кодом, добавляя номер телефона в параметры запроса
        return reverse_lazy('interface:sms_code') + '?phone=' + self.object.phone

    def form_valid(self, form, *args, **kwargs):
        return_data = {}

        form.is_valid()
        user = form.save()  # Сохраняем пользователя из валидной формы
        user.invite_code = create_unique_invite_code()  # Генерируем и присваиваем инвайт-код
        return_data['invite_code'] = user.invite_code

        password = generate_sms_code()  # Генерируем временный пароль
        user.set_password(password)  # Устанавливаем сгенерированный пароль

        # Отправляем SMS с временным кодом
        # sms_response = send(int(user.phone), f'Ваш код: {password}')  # Убедитесь, что номер телефона хранится в user.phone
        user.save()  # Сохраняем изменения в пользователе

        return super().form_valid(form)  # Переход к следующему шагу

    def form_invalid(self, form, *args, **kwargs):
        # Если форма невалидна, пытаемся получить уже существующего пользователя
        user = User.objects.get(phone=form.data.get('phone'))

        password = generate_sms_code()  # Генерируем новый пароль
        user.set_password(password)  # Устанавливаем новый пароль

        # sms_response = send(int(user.phone), f'Ваш код: {password}')  # Убедитесь, что используется правильный номер
        user.save()  # Сохраняем пользователя

        self.object = user  # Обновляем объект пользователя
        return redirect(self.get_success_url())  # Переход к следующему шагу


class SmsCodeView(View):
    """Проверка кода из SMS и авторизация пользователя"""

    def post(self, *args, **kwargs):
        phone = self.request.POST.get('phone')  # Получаем номер телефона из POST-запроса
        code = self.request.POST.get('code')  # Получаем код из POST-запроса
        user = authenticate(self.request, username=phone, password=code)  # Проверяем пользователя
        if user is not None:
            login(self.request, user)  # Если пользователь аутентифицирован, выполняем вход
            # Перенаправляем на страницу с успехом после логина
            return redirect(reverse('interface:user_detail'))
        else:
            # Если аутентификация не прошла, перенаправляем на страницу логина
            return redirect(reverse('interface:login'))

    def get(self, *args, **kwargs):
        form = SmsCodeForm()  # Создаем экземпляр формы для ввода кода
        return render(self.request, 'interface/sms_code.html', {'form': form})  # Отображаем форму


class UserDetailView(DetailView):
    """Отображение данных пользователя"""

    model = User  # Модель для отображения данных
    template_name = 'interface/user_detail.html'  # Шаблон для показа деталей пользователя

    def get_object(self, queryset=None):
        # Получаем текущего пользователя из запроса
        return self.request.user


class UserUpdateView(UpdateView):
    """Обновление данных пользователя"""

    model = User  # Модель для обновления данных
    template_name = 'interface/user_form.html'  # Шаблон для формы обновления
    form_class = UserUpdateForm  # Форма для обновления данных пользователя
    success_url = reverse_lazy('interface:user_detail')  # URL для перенаправления после успешного обновления

    def get_object(self, queryset=None):
        # Получаем текущего пользователя для обновления его данных
        return self.request.user

    def get_success_url(self):
        # Формируем URL для перенаправления, добавляя номер телефона в параметры запроса
        return reverse_lazy('interface:user_detail') + '?phone=' + self.object.phone

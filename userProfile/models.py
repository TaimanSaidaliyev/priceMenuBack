from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from establishment.models import Establishment


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='profile')
    fathers_name = models.CharField(max_length=30, blank=True, verbose_name='Отчество')
    company = models.ForeignKey(Establishment, null=True, blank=True, on_delete=models.PROTECT, verbose_name='Заведение', related_name='profile_establishment')
    telephone = models.CharField(max_length=30, blank=True, verbose_name='Контактный телефон')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    def __str__(self):
        return str(self.user.first_name + ' ' + self.user.last_name)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профиль'
        ordering = ['-created_date']
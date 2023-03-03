from django.db import models
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField


class Mailing(models.Model):
    start_mailing = models.DateTimeField(verbose_name='Дата начала рассылки')
    finish_mailing = models.DateTimeField(verbose_name='Дата окончания рассылки')
    text_message = models.TextField(blank=True, verbose_name='Текст сообщения')
    # filter_teg = models.ManyToManyField('Teg', verbose_name='Фильтр по тегу', blank=True)
    # filter_code = models.ManyToManyField('Code_operators', verbose_name='Фильтр по коду опер.', blank=True)

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'


class Clients(models.Model):

    VIP = 'ВИП'
    DONT_WORRY = 'Не беспокоить'
    NORMAL = 'Обычный'
    TEGS = [
        (VIP, 'ВИП'),
        (DONT_WORRY, 'Не беспокоить'),
        (NORMAL, 'Обычный'),
    ]

    TZ = [
        (1, '-10'),
        (2, '-9'),
        (3, '-8'),
        (4, '-7'),
        (5, '-6'),
        (6, '-5'),
        (7, '-4'),
        (8, '-3'),
        (9, '-2'),
        (10, '-1'),
        (11, '0'),
        (12, '+1'),
        (13, '+2'),
        (14, '+3'),
        (15, '+4'),
        (16, '+5'),
        (17, '+6'),
        (18, '+7'),
        (19, '+8'),
        (20, '+9'),
        (21, '+10'),
        (22, '+11'),
        (23, '+12'),
        (24, '+13'),
        (25, '+14'),
    ]
    phone = PhoneNumberField(null=False, blank=False, unique=True, region="RU", verbose_name='phone')
    teg = models.CharField(max_length=15, choices=TEGS, verbose_name='Тег', default=NORMAL)
    code_operator = models.IntegerField(verbose_name='Код моб. оператора')
    time_zone = models.IntegerField(choices=TZ, verbose_name='UTC', default=14)

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ['phone']


class Messages(models.Model):
    time_maling = models.DateTimeField(verbose_name='Дата отправки')
    status = models.IntegerField(default=0, verbose_name='Статус')
    id_clients = models.ForeignKey(Clients, on_delete=models.CASCADE, verbose_name='id Клиента')
    id_mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, verbose_name='id Рассылки')


    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'


class Status(models.Model):
    status = models.BooleanField(default=0, verbose_name='Статус')
    mailings_id = models.ForeignKey(Mailing, on_delete=models.CASCADE)


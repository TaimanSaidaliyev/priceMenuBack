from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Country(models.Model):
    title = models.CharField(max_length=99, verbose_name='Страна')
    coordinate_w = models.FloatField(default=0, blank=False, null=False, verbose_name='Ширина')
    coordinate_h = models.FloatField(default=0, blank=False, null=False, verbose_name='Долгота')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страна'
        ordering = ['-created_at']


class City(models.Model):
    title = models.CharField(max_length=99, verbose_name='Город')
    coordinate_w = models.FloatField(default=0, blank=False, null=False, verbose_name='Ширина')
    coordinate_h = models.FloatField(default=0, blank=False, null=False, verbose_name='Долгота')
    country = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, verbose_name='Страна', related_name='city_country')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Город'
        ordering = ['-created_at']


class PremiumStatus(models.Model):
    title = models.CharField(max_length=99, verbose_name='Название статуса')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статус заведения'
        verbose_name_plural = 'Статус заведения'
        ordering = ['-created_at']


class TypeOfEstablishment(models.Model):
    title = models.CharField(max_length=100, db_index=True, verbose_name='Тип заведения')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', verbose_name='Изображение', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тип заведения'
        verbose_name_plural = 'Тип заведения'
        ordering = ['title']


class Establishment(models.Model):
    SQUARE = 'Square'
    LIST = 'List'
    MENU_VIEW_CHOICES = [
        (SQUARE, 'Квадратные плиты'),
        (LIST, 'Списком'),
    ]
    title = models.CharField(max_length=99, verbose_name='Название заведения')
    default_color = models.CharField(max_length=7, verbose_name='Цвет заведения')
    secondary_color = models.BooleanField(default=True, verbose_name='Вторичный цвет (Белый)')
    description = models.TextField(max_length=500, verbose_name='Описание заведения')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', verbose_name='Изображение', blank=True)
    backgroundImage = models.ImageField(upload_to='photos/%Y/%m/%d', verbose_name='Фоновое изображение', blank=True)
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    rating = models.FloatField(default=0, verbose_name='Рейтинг заведения')
    coordinate_w = models.FloatField(default=0, blank=False, null=False, verbose_name='Ширина')
    coordinate_h = models.FloatField(default=0, blank=False, null=False, verbose_name='Долгота')
    city = models.ForeignKey(City, on_delete=models.CASCADE, blank=True, verbose_name='Город', related_name='shop_city')
    address = models.CharField(max_length=2000, verbose_name='Адрес заведения')
    workTime = models.CharField(max_length=99, verbose_name='Режим работы заведения')
    phoneNumber = models.CharField(max_length=99, verbose_name='Телефон')
    premium_status = models.ForeignKey(PremiumStatus, on_delete=models.PROTECT, blank=True, null=True, verbose_name='Премиум статус заведения', related_name='get_establishment_status')
    type_of_establishment = models.ForeignKey(TypeOfEstablishment, on_delete=models.PROTECT, blank=True, null=True, verbose_name='Тип заведения', related_name='get_type_of_establishment')
    menu_view_type = models.CharField(max_length=10, choices=MENU_VIEW_CHOICES, default=LIST, verbose_name='Вид меню')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Заведение'
        verbose_name_plural = 'Заведение'
        ordering = ['-created_at']


class Menu(models.Model):
    menu_title = models.CharField(max_length=100, db_index=True, verbose_name='Меню')
    photo = models.ImageField(upload_to='photos/category/%Y/%m/%d', verbose_name='Изображение', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    establishment = models.ForeignKey(Establishment, on_delete=models.PROTECT, blank=True, null=True, verbose_name='Заведение', related_name='get_menu_establishment')
    sorting_number = models.IntegerField(default=0, blank=True, null=True, verbose_name='Порядок сортировки')

    def __str__(self):
        return self.menu_title

    class Meta:
        verbose_name = 'Меню заведения'
        verbose_name_plural = 'Меню заведения'
        ordering = ['-created_at']


class MenuCategory(models.Model):
    category_title = models.CharField(max_length=100, db_index=True, verbose_name='Категории')
    photo = models.ImageField(upload_to='photos/category/%Y/%m/%d', verbose_name='Изображение', blank=True)
    menu = models.ForeignKey(Menu, on_delete=models.PROTECT, blank=True, null=True, verbose_name='Меню', related_name='get_menu_category_menu')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    establishment = models.ForeignKey(Establishment, on_delete=models.PROTECT, blank=True, null=True,
                                      verbose_name='Заведение', related_name='get_menu_category_establishment')
    sorting_number = models.IntegerField(default=0, blank=True, null=True, verbose_name='Порядок сортировки')

    def __str__(self):
        return self.category_title

    class Meta:
        verbose_name = 'Категория меню'
        verbose_name_plural = 'Категория меню'
        ordering = ['-category_title']

    class MPTTMeta:
        order_insertion_by = ['created_at']


class Products (models.Model):
    title = models.CharField(max_length=99, verbose_name='Название блюда')
    description = models.TextField(max_length=500, verbose_name='Описание блюда')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    price = models.FloatField(default=0, blank=False, null=False, verbose_name='Текущая цена')
    old_price = models.FloatField(default=0, blank=False, null=False, verbose_name='Старая цена')
    photo = models.ImageField(upload_to='photo/products/%Y/%m/%d', verbose_name='Изображение', blank=True)
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    is_active = models.BooleanField(default=True, verbose_name='Есть на кухне')
    category = models.ForeignKey(MenuCategory, on_delete=models.PROTECT, verbose_name='Категория', related_name='get_products_menu_category')
    establishment = models.ForeignKey(Establishment, on_delete=models.PROTECT, blank=True, null=True,
                                      verbose_name='Заведение', related_name='get_products_establishment')
    sorting_number = models.IntegerField(default=0, blank=True, null=True, verbose_name='Порядок сортировки')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Блюда'
        verbose_name_plural = 'Блюда'
        ordering = ['-created_at']


class Promotions(models.Model):
    BANNER = 'Banner'
    LABEL = 'Label'
    TYPE_CHOICES = [
        (BANNER, 'Баннер'),
        (LABEL, 'Надпись'),
    ]

    title = models.CharField(max_length=100, db_index=True, verbose_name='Название акции')
    description = models.TextField(max_length=300, db_index=True, verbose_name='Описание акции')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', verbose_name='Изображение', blank=True)
    until_date = models.DateField(verbose_name='Дата истечения срока')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    promotion_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default=BANNER, verbose_name='Тип акции')
    establishment = models.ForeignKey(Establishment, on_delete=models.PROTECT, blank=True, null=True,
                                      verbose_name='Заведение', related_name='get_promotions_establishment')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Акции'
        verbose_name_plural = 'Акции'
        ordering = ['created_at']
from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw

import uuid


class Category(models.Model):
    title = models.CharField(max_length=100)
    title_en = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f'{self.title}'


class Dish(models.Model):
    category = models.ForeignKey(Category, related_name='dishes', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    ingredients = models.CharField(max_length=2000)
    allergens = models.CharField(max_length=2000, blank=True)
    name_en = models.CharField(max_length=100, blank=True)
    ingredients_en = models.CharField(max_length=2000, blank=True)
    quantity = models.IntegerField(default=300)
    price = models.FloatField()
    image = models.ImageField(upload_to='images/', blank=True)

    class Meta:
        verbose_name_plural = 'Dishes'

    def __str__(self):
        return f'{self.name}'


class QrCode(models.Model):
    name = models.CharField(max_length=200)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True)

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        qrcode_img = qrcode.make(self.name)
        canvas = Image.new('RGB', (400, 400), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.name}.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)


class Table(models.Model):
    url = models.UUIDField(default=uuid.uuid4)
    unconfirmed_orders = models.TextField(null=True, default='[]')
    confirmed_orders = models.TextField(null=True, default='[]')
    check = models.FloatField(default=0)
    QR = models.ForeignKey(QrCode, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return f'{self.id}'


class Comment(models.Model):
    comment = models.TextField()
    time_added = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        ordering = ('-time_added', )

    def __str__(self):
        return f'{self.time_added}'


class Allergen(models.Model):
    name = models.CharField(max_length=100)
    name_en = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'

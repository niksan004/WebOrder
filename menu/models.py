from django.db import models
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw

import uuid


class Category(models.Model):
    category = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.category}'


class Dish(models.Model):
    name = models.CharField(max_length=100)
    ingredients = models.CharField(max_length=2000)
    quantity = models.IntegerField(default=300)
    price = models.FloatField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', blank=True)

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

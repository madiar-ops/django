from django.db import models
from decimal import Decimal
from django.db.models import Sum
from .validators import non_negative


class Rubric(models.Model):
    name = models.CharField(max_length=20, db_index=True, verbose_name='Название')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Рубрика'
        verbose_name_plural = 'Рубрики'
        ordering = ('name',)


class Bb(models.Model):
    title = models.CharField(max_length=50, verbose_name='Товар')
    content = models.TextField(null=True, blank=True, verbose_name='Описание')
    price = models.FloatField(null=True, blank=True, verbose_name='Цена')
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано')
    rubric = models.ForeignKey(
        Rubric,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        verbose_name='Рубрика'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Обьявление'
        verbose_name_plural = 'Обьявления'
        ordering = ('-published',)



class IceCreamKiosk(models.Model):
    name = models.CharField("Название киоска", max_length=120)
    address = models.CharField("Адрес", max_length=255)
    is_open = models.BooleanField("Открыт", default=True)

    def id_and_name(self):
        return f"{self.id} — {self.name}"

    def total_icecream_price(self):
        return self.ice_creams.aggregate(total=Sum("price"))["total"] or Decimal("0.00")

    def in_stock_count(self):
        return self.ice_creams.filter(in_stock=True).count()

    def __str__(self):
        return f"{self.name} ({self.address})"


class IceCream(models.Model):
    kiosk = models.ForeignKey(
        IceCreamKiosk,
        on_delete=models.CASCADE,
        related_name="ice_creams",
        verbose_name="Киоск"
    )
    title = models.CharField("Название", max_length=120)
    flavor = models.CharField("Вкус", max_length=120)
    price = models.DecimalField("Цена", max_digits=8, decimal_places=2)
    in_stock = models.BooleanField("В наличии", default=True)
    price = models.DecimalField(
        "Цена",
        max_digits=8,
        decimal_places=2,
        validators=[non_negative]
    )

    def id_and_title(self):
        return f"{self.id} — {self.title}"
    def __str__(self):
        return f"{self.title} — {self.flavor} ({self.price})"


class Parent(models.Model):
    full_name = models.CharField("ФИО родителя", max_length=150)
    phone = models.CharField("Телефон", max_length=30, blank=True)

    def __str__(self):
        return self.full_name


class Child(models.Model):
    parent = models.ForeignKey(
        Parent,
        on_delete=models.CASCADE,
        related_name="children",
        verbose_name="Родитель"
    )
    full_name = models.CharField("ФИО ребёнка", max_length=150)
    age = models.PositiveIntegerField("Возраст", validators=[non_negative])

    def __str__(self):
        return f"{self.full_name} ({self.age})"

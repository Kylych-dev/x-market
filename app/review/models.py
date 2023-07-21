from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField
from app.product.models import Product

User = get_user_model()


class Review(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    rating = models.PositiveIntegerField(_("rating"), validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = RichTextField(_("comment"), default="", blank=False)
    created_at = models.DateField(_("created_at"), auto_now_add=True)
    updated_at = models.DateField(_("updated_at"), auto_now=True)

    class Meta:
        abstract = True


class ProductReview(Review):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, related_name="product_review")

    class Meta:
        verbose_name = "Отзыв на Продукт"
        verbose_name_plural = "Отзывы на Продукт"


class CourierReview(Review):
    courier = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name="employee_review")

    class Meta:
        verbose_name = "Отзыв на Сотрудника"
        verbose_name_plural = "Отзывы на Сотрудника"


class Reply(models.Model):
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    comment = RichTextField(_("comment"), default="", blank=False)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    created_at = models.DateField(_("created_at"), auto_now_add=True)
    updated_at = models.DateField(_("updated_at"), auto_now=True)

    class Meta:
        abstract = True


class ReplyOnProductReview(Reply):
    review = models.ForeignKey(ProductReview, on_delete=models.CASCADE, null=True,
                               related_name="reply_on_product_review")

# Generated by Django 4.2.2 on 2023-07-14 14:13

import ckeditor.fields
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('review', '0002_alter_employeereview_comment_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourierReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='rating')),
                ('comment', ckeditor.fields.RichTextField(default='', verbose_name='comment')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created_at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated_at')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('courier', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='employee_review', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Отзыв на Сотрудника',
                'verbose_name_plural': 'Отзывы на Сотрудника',
            },
        ),
        migrations.DeleteModel(
            name='EmployeeReview',
        ),
    ]

# Generated by Django 4.2.2 on 2023-07-16 07:33

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('category', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('description', ckeditor.fields.RichTextField()),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('capacity', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('is_favorite', models.BooleanField(default=False)),
                ('image', models.ImageField(blank=True, null=True, upload_to='products_image/')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='category.category')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
        ),
    ]

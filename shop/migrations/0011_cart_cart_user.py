# Generated by Django 5.0.6 on 2024-06-18 18:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_remove_cart_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='cart_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cart', to='shop.user'),
        ),
    ]

# Generated by Django 3.2.9 on 2023-08-25 15:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pizzaapp', '0005_alter_cart_items'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='user_id',
            new_name='user',
        ),
    ]

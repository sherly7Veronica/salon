# Generated by Django 4.1.5 on 2023-01-13 22:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_orderdetail'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='user',
        ),
    ]

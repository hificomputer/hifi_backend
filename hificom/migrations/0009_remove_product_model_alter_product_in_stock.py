# Generated by Django 4.2 on 2024-07-07 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hificom', '0008_remove_productimage_thumbnail_alter_keyfeature_value'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='model',
        ),
        migrations.AlterField(
            model_name='product',
            name='in_stock',
            field=models.BooleanField(default=True),
        ),
    ]

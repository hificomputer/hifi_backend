# Generated by Django 4.2 on 2024-07-16 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hificom', '0017_alter_carousel_options_alter_carousel_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcollection',
            name='slug',
            field=models.CharField(db_index=True, max_length=100, unique=True),
        ),
    ]

# Generated by Django 4.2 on 2024-07-14 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hificom', '0012_alter_categorygroup_options_alter_category_cat_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='short_title',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]

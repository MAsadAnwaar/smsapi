# Generated by Django 4.2 on 2023-06-21 05:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userdata', '0016_sub_category_sub_cat_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='language',
        ),
        migrations.DeleteModel(
            name='lang',
        ),
    ]

# Generated by Django 4.2 on 2023-08-07 06:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userdata', '0019_sub_category_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sub_category',
            name='title',
        ),
    ]
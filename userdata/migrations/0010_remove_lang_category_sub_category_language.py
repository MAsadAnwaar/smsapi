# Generated by Django 4.2 on 2023-06-01 07:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userdata', '0009_remove_category_language_lang_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lang',
            name='category',
        ),
        migrations.AddField(
            model_name='sub_category',
            name='language',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='userdata.lang'),
            preserve_default=False,
        ),
    ]

# Generated by Django 4.2 on 2023-06-01 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userdata', '0007_complaint_max_complaints'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='language',
        ),
        migrations.AddField(
            model_name='category',
            name='language',
            field=models.ManyToManyField(to='userdata.lang'),
        ),
    ]

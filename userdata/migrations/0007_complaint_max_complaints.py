# Generated by Django 4.2 on 2023-04-27 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userdata', '0006_remove_complaint_max_complaints'),
    ]

    operations = [
        migrations.AddField(
            model_name='complaint',
            name='max_complaints',
            field=models.PositiveIntegerField(default=5),
        ),
    ]
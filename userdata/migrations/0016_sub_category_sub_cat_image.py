# Generated by Django 4.2 on 2023-06-15 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userdata', '0015_sms_dislikes_sms_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='sub_category',
            name='Sub_cat_image',
            field=models.ImageField(blank=True, upload_to='Sub_cat_image'),
        ),
    ]
# Generated by Django 4.1.7 on 2023-04-01 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0017_merge_20230331_0833'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='photos', verbose_name='Фото'),
        ),
        migrations.AddField(
            model_name='coach',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='photos', verbose_name='Фото'),
        ),
    ]

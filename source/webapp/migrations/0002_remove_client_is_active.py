# Generated by Django 4.1.7 on 2023-02-25 11:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='client',
            name='is_active',
        ),
    ]
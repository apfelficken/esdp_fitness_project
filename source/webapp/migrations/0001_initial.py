# Generated by Django 4.1.7 on 2023-02-25 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_name', models.CharField(max_length=50, verbose_name='Telegram')),
                ('phone', models.CharField(blank=True, max_length=20, null=True, verbose_name='Phone')),
                ('first_name', models.CharField(max_length=20, verbose_name='Name')),
                ('last_name', models.CharField(max_length=20, verbose_name='Family_name')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email')),
                ('is_active', models.BooleanField(default=False, verbose_name='Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('payment_at', models.DateTimeField(blank=True, null=True, verbose_name='Payment')),
            ],
        ),
    ]

# Generated by Django 4.2.3 on 2023-07-17 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0005_delete_chatroom'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('url', models.CharField(max_length=100, unique=True)),
            ],
        ),
    ]
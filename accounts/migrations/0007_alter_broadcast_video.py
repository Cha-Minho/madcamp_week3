# Generated by Django 4.2.3 on 2023-07-17 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_broadcast_video'),
    ]

    operations = [
        migrations.AlterField(
            model_name='broadcast',
            name='video',
            field=models.FileField(upload_to=''),
        ),
    ]

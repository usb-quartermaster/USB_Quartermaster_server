# Generated by Django 3.0.1 on 2019-12-22 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='driver',
            field=models.CharField(choices=[('UsbipOverSSH', 'UsbipOverSSH'), ('VirtualHereOverSSH', 'VirtualHereOverSSH')], max_length=100),
        ),
    ]

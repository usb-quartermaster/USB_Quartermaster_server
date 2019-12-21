# Generated by Django 2.2.7 on 2019-11-26 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0008_auto_20191120_0046'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device',
            name='id',
        ),
        migrations.AlterField(
            model_name='device',
            name='driver',
            field=models.CharField(choices=[('VirtualHere', 'VirtualHere')], max_length=100),
        ),
        migrations.AlterField(
            model_name='device',
            name='name',
            field=models.SlugField(max_length=30, primary_key=True, serialize=False),
        ),
    ]
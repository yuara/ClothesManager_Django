# Generated by Django 3.1.1 on 2020-09-03 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20200902_1250'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='color',
            field=models.CharField(default='430c7a', max_length=6),
        ),
    ]

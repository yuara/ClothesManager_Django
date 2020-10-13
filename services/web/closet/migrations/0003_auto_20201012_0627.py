# Generated by Django 3.1.2 on 2020-10-12 06:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('closet', '0002_auto_20201011_0251'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='color',
            name='proportion',
        ),
        migrations.AlterField(
            model_name='color',
            name='clothes',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='colors', to='closet.clothes'),
        ),
        migrations.AlterField(
            model_name='color',
            name='code',
            field=models.CharField(max_length=64, null=True, verbose_name='code'),
        ),
    ]
# Generated by Django 3.1.3 on 2020-11-16 02:36

import accounts.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='area',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.PROTECT, to='accounts.area'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='color',
            field=models.CharField(blank=True, default=accounts.models.set_random_color, max_length=6),
        ),
        migrations.AlterField(
            model_name='profile',
            name='prefecture',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.PROTECT, to='accounts.prefecture'),
        ),
    ]

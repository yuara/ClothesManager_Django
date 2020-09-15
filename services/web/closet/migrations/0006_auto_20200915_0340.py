# Generated by Django 3.1.1 on 2020-09-15 03:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('closet', '0005_auto_20200915_0329'),
    ]

    operations = [
        migrations.CreateModel(
            name='Weather',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('icon', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='forecast',
            name='weather',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='closet.weather'),
        ),
    ]
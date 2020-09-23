# Generated by Django 3.1.1 on 2020-09-23 04:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='area')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='category name')),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
        ),
        migrations.CreateModel(
            name='Clothes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, verbose_name='name')),
                ('note', models.TextField(blank=True, verbose_name='note')),
                ('picture', models.ImageField(blank=True, upload_to='clothes_pic/')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date created')),
                ('publish', models.BooleanField(default=False, verbose_name='publish')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='clothes', to='closet.category', verbose_name='category')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='clothes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'clothes',
                'verbose_name_plural': 'clothes',
            },
        ),
        migrations.CreateModel(
            name='ClothesIndex',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.PositiveIntegerField(verbose_name='value')),
                ('description', models.TextField(blank=True, verbose_name='description')),
            ],
            options={
                'verbose_name': 'clothes index',
                'verbose_name_plural': 'clothes indexes',
            },
        ),
        migrations.CreateModel(
            name='ParentCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='parent category name')),
            ],
            options={
                'verbose_name': 'parent category',
                'verbose_name_plural': 'parent categories',
            },
        ),
        migrations.CreateModel(
            name='Weather',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('icon', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Prefecture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='prefecture')),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='closet.area', verbose_name='area')),
            ],
        ),
        migrations.CreateModel(
            name='Outfit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, verbose_name='name')),
                ('note', models.TextField(blank=True, verbose_name='note')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date created')),
                ('publish', models.BooleanField(default=False, verbose_name='publish')),
                ('bottom', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='bottom', to='closet.clothes', verbose_name='bottom')),
                ('extra_top', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='extra_top', to='closet.clothes', verbose_name='extra top')),
                ('outerwear', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='outerwear', to='closet.clothes', verbose_name='outerwear')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='outfits', to=settings.AUTH_USER_MODEL)),
                ('top', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='top', to='closet.clothes', verbose_name='top')),
            ],
        ),
        migrations.CreateModel(
            name='IndexCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('needs_outers', models.BooleanField(default=False, verbose_name='needs_outers')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='closet.category')),
                ('clothes_index', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='closet.clothesindex')),
            ],
            options={
                'verbose_name': 'index category',
                'verbose_name_plural': 'index categories',
            },
        ),
        migrations.CreateModel(
            name='Forecast',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('highest_temp', models.IntegerField(verbose_name='highest tempreture')),
                ('lowest_temp', models.IntegerField(verbose_name='lowest tempreture')),
                ('rain_chance', models.IntegerField(verbose_name='rain chance')),
                ('created_at', models.DateTimeField(verbose_name='date created')),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='forecast', to='closet.area', verbose_name='area')),
                ('clothes_index', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='forecast', to='closet.clothesindex', verbose_name='clothes index')),
                ('prefecture', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='forecast', to='closet.prefecture', verbose_name='prefecture')),
                ('weather', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='closet.weather')),
            ],
        ),
        migrations.AddField(
            model_name='clothesindex',
            name='categories',
            field=models.ManyToManyField(blank=True, through='closet.IndexCategory', to='closet.Category'),
        ),
        migrations.AddField(
            model_name='clothes',
            name='parent_category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='parent_category', to='closet.parentcategory', verbose_name='parent category'),
        ),
        migrations.AddField(
            model_name='category',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='child', to='closet.parentcategory', verbose_name='parent category'),
        ),
    ]

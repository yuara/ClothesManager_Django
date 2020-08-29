# Generated by Django 3.1 on 2020-08-25 04:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FollowUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following_followusers', to=settings.AUTH_USER_MODEL)),
                ('following', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower_followusers', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('follower', 'following')},
            },
        ),
        migrations.AddField(
            model_name='user',
            name='followers',
            field=models.ManyToManyField(related_name='_user_followers_+', through='accounts.FollowUser', to=settings.AUTH_USER_MODEL, verbose_name='followers'),
        ),
        migrations.AddField(
            model_name='user',
            name='followings',
            field=models.ManyToManyField(related_name='_user_followings_+', through='accounts.FollowUser', to=settings.AUTH_USER_MODEL, verbose_name='following users'),
        ),
    ]
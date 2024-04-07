# Generated by Django 5.0.2 on 2024-04-06 15:46

import django.db.models.deletion
import userprofiles.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('avatar', models.ImageField(blank=True, default='users/default/avatar_default.png', upload_to=userprofiles.models.media_directory_path)),
                ('background', models.ImageField(blank=True, default='users/default/background_default.jpg', upload_to=userprofiles.models.media_directory_path)),
                ('_destroy', models.BooleanField(default=False)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
            options={
                'indexes': [models.Index(fields=['user_id'], name='userprofile_user_id_03ed93_idx')],
            },
        ),
        migrations.CreateModel(
            name='LinkProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(max_length=255)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
            options={
                'indexes': [models.Index(fields=['user_id'], name='userprofile_user_id_011e75_idx')],
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('phone', models.CharField(max_length=15, null=True)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('gender', models.CharField(max_length=10)),
                ('address', models.CharField(blank=True, max_length=255)),
                ('bio', models.TextField(blank=True)),
                ('school', models.CharField(blank=True, max_length=255)),
                ('work', models.CharField(blank=True, max_length=255)),
                ('_destroy', models.BooleanField(default=False)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
            options={
                'indexes': [models.Index(fields=['user_id'], name='userprofile_user_id_e911da_idx')],
            },
        ),
    ]

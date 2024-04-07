# Generated by Django 5.0.2 on 2024-04-06 15:46

import django.db.models.deletion
import posts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, null=True)),
                ('content', models.TextField(null=True)),
                ('status', models.CharField(default='public', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
        ),
        migrations.CreateModel(
            name='MediaOfPosts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media', models.FileField(upload_to=posts.models.post_directory_path)),
                ('post_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.posts')),
            ],
        ),
        migrations.AddIndex(
            model_name='posts',
            index=models.Index(fields=['user_id'], name='posts_posts_user_id_fd2973_idx'),
        ),
        migrations.AddIndex(
            model_name='posts',
            index=models.Index(fields=['id'], name='posts_posts_id_d311f0_idx'),
        ),
        migrations.AddIndex(
            model_name='mediaofposts',
            index=models.Index(fields=['post_id'], name='posts_media_post_id_9bec13_idx'),
        ),
    ]

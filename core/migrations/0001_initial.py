# Generated by Django 5.0.2 on 2024-03-12 14:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('blog_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('body', models.TextField()),
                ('status', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('chat_id', models.AutoField(primary_key=True, serialize=False)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('username', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=1000)),
                ('avatar', models.CharField(default='user-default.png', max_length=255, null=True)),
                ('background', models.CharField(default='unnamed.jpg', max_length=255, null=True)),
                ('DOB', models.CharField(max_length=50)),
                ('place', models.CharField(max_length=255)),
                ('school', models.CharField(max_length=255)),
                ('company', models.CharField(max_length=255)),
                ('last_seen', models.DateTimeField(auto_now=True)),
                ('phone', models.CharField(max_length=16)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('like_id', models.AutoField(primary_key=True, serialize=False)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.blog')),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.user')),
            ],
        ),
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('friend_id', models.AutoField(primary_key=True, serialize=False)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('friend_id_1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend1', to='core.user')),
                ('friend_id_2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='friend2', to='core.user')),
            ],
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('followed_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followed', to='core.user')),
                ('following_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to='core.user')),
            ],
        ),
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('conversation_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=40)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.user')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.user'),
        ),
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('chat_id', models.AutoField(primary_key=True, serialize=False)),
                ('message', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('conversation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.conversation')),
                ('from_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_chats', to='core.user')),
                ('to_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_chats', to='core.user')),
            ],
        ),
        migrations.AddField(
            model_name='blog',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.user'),
        ),
    ]

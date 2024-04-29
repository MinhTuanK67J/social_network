# Generated by Django 4.2.11 on 2024-04-28 15:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('posts', '0002_alter_mediaofposts_media_alter_posts_content_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostIsWatched',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_watched', models.BooleanField(default=False)),
                ('post_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.posts')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.user')),
            ],
            options={
                'indexes': [models.Index(fields=['post_id', 'user_id'], name='posts_posti_post_id_936162_idx')],
            },
        ),
    ]

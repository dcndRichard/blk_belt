# Generated by Django 2.2 on 2019-12-20 19:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blk_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quote', models.TextField(max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('users_who_liked', models.ManyToManyField(related_name='likes', to='blk_app.User')),
                ('users_who_posted', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post', to='blk_app.User')),
            ],
        ),
        migrations.DeleteModel(
            name='Wish',
        ),
    ]

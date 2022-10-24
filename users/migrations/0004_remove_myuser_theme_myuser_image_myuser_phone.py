# Generated by Django 4.0.6 on 2022-10-24 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_myuser_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myuser',
            name='theme',
        ),
        migrations.AddField(
            model_name='myuser',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='profile_pics'),
        ),
        migrations.AddField(
            model_name='myuser',
            name='phone',
            field=models.CharField(default=1, max_length=20),
            preserve_default=False,
        ),
    ]

# Generated by Django 3.0.4 on 2020-03-07 18:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subreddit', '0006_auto_20200307_1503'),
    ]

    operations = [
        migrations.AlterField(
            model_name='linkpost',
            name='thumbnail',
            field=models.ImageField(default='img\\link_default.png', height_field='thumbnail_height', upload_to='thumbnail', width_field='thumbnail_width'),
        ),
        migrations.AlterField(
            model_name='selfpost',
            name='thumbnail',
            field=models.ImageField(default='img\\self_default.png', height_field='thumbnail_height', upload_to='thumbnail', width_field='thumbnail_width'),
        ),
    ]

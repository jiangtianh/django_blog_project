# Generated by Django 4.2.5 on 2023-09-08 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='title_tag',
            field=models.CharField(default='default', max_length=255),
            preserve_default=False,
        ),
    ]
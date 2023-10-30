# Generated by Django 4.2.5 on 2023-09-10 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_blog', '0003_post_post_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='post_date',
            new_name='post_created_date',
        ),
        migrations.AddField(
            model_name='post',
            name='post_updated_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
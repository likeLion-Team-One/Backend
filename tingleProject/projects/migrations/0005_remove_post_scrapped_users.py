# Generated by Django 5.2.3 on 2025-06-21 13:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='scrapped_users',
        ),
    ]

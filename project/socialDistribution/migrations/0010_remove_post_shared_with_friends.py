# Generated by Django 4.2.4 on 2023-10-29 23:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialDistribution', '0009_alter_author_profileimage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='shared_with_friends',
        ),
    ]

# Generated by Django 4.2.4 on 2023-11-25 09:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialDistribution', '0019_alter_post_categories'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='parentPost',
            new_name='post',
        ),
    ]

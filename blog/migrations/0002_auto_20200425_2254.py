# Generated by Django 3.0.3 on 2020-04-25 14:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blog',
            options={'ordering': ['-created_time']},
        ),
        migrations.RenameField(
            model_name='blog',
            old_name='Blog_type',
            new_name='blog_type',
        ),
    ]

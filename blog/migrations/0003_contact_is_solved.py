# Generated by Django 5.0.3 on 2024-03-11 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='is_solved',
            field=models.BooleanField(default=False),
        ),
    ]

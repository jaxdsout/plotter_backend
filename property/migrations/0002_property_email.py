# Generated by Django 5.1 on 2024-08-28 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='email',
            field=models.EmailField(default=None, max_length=250),
            preserve_default=False,
        ),
    ]

# Generated by Django 5.1 on 2024-08-30 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agent', '0008_alter_option_sq_ft'),
    ]

    operations = [
        migrations.AddField(
            model_name='list',
            name='link_url',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]

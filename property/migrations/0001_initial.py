# Generated by Django 5.1 on 2024-08-14 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('image', models.ImageField(blank=True, upload_to='')),
                ('website', models.CharField(max_length=250)),
                ('market', models.CharField(choices=[('hou', 'Houston'), ('dfw', 'Dallas / Fort Worth'), ('atx', 'Austin')], default='hou', max_length=100)),
                ('neighborhood', models.CharField(max_length=250)),
                ('address', models.CharField(max_length=250)),
                ('latitude', models.CharField(max_length=100)),
                ('longitude', models.CharField(max_length=100)),
            ],
        ),
    ]

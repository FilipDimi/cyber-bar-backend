# Generated by Django 3.2.16 on 2023-06-09 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cocktail',
            name='color',
            field=models.CharField(default='#ff5335', max_length=10),
        ),
    ]

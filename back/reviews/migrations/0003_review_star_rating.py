# Generated by Django 4.2.16 on 2024-11-21 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_reviewlike'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='star_rating',
            field=models.FloatField(default=0.0),
        ),
    ]

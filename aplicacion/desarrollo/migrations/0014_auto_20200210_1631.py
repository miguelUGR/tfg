# Generated by Django 2.2.6 on 2020-02-10 16:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('desarrollo', '0013_auto_20200210_1612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='usuarios/'),
        ),
    ]

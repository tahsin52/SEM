# Generated by Django 4.1.4 on 2022-12-24 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='carmodel',
            name='transmission',
            field=models.CharField(max_length=155, null=True),
        ),
    ]

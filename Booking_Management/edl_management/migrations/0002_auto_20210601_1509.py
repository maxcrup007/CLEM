# Generated by Django 3.0 on 2021-06-01 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edl_management', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lab',
            old_name='picture',
            new_name='photo',
        ),
        migrations.AlterField(
            model_name='lab',
            name='name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]

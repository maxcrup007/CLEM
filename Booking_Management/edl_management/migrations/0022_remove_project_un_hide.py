# Generated by Django 3.0 on 2021-06-20 09:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('edl_management', '0021_auto_20210620_1648'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='un_hide',
        ),
    ]

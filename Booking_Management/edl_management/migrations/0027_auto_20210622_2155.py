# Generated by Django 3.0 on 2021-06-22 14:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('edl_management', '0026_auto_20210622_2153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookequipmentletter',
            name='project',
            field=models.ForeignKey(blank=True, help_text='โครงการที่ทำอยู่', null=True, on_delete=django.db.models.deletion.CASCADE, to='edl_management.Project'),
        ),
    ]

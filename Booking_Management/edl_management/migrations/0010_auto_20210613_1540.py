# Generated by Django 3.0 on 2021-06-13 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('edl_management', '0009_auto_20210613_1531'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='applicant_status',
        ),
        migrations.AddField(
            model_name='project',
            name='example',
            field=models.CharField(blank=True, help_text='สารตัวอย่างที่นำมา Freeze dry เช่น สารสกัดสมุนไพร, ชิ้นผลไม้, ข้าว (หากเป็นชิ้นงาน ควรจะมีขนาดหนาไม่เกิน 2 cm.)', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='substance',
            field=models.IntegerField(blank=True, help_text='ปริมาณสารทั้งหมดที่นำมาใช้ Freeze dry (เนื่องจากต้องมีปริมาณน้ำที่จำกัดในการFreeze dry อยู่ที่ไม่เกิน 2000 ml. ต่อการทำแห้ง 1 รอบ) ', null=True),
        ),
    ]

# Generated by Django 3.1.4 on 2021-04-02 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TechnoApp', '0008_auto_20210402_1048'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coilstatus',
            name='status_class',
            field=models.CharField(choices=[('PRODUCTION', 'PRODUCTION'), ('ENALING', 'ENALING'), ('DRAW', 'DRAW')], default='PRODUCTION', max_length=15),
        ),
    ]

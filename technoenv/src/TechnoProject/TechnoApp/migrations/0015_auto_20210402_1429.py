# Generated by Django 3.1.4 on 2021-04-02 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TechnoApp', '0014_auto_20210402_1322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coilstatus',
            name='status_class',
            field=models.CharField(choices=[('IN PRODUCTION', 'IN PRODUCTION'), ('ANNEALING', 'ANNENALING'), ('DRAW', 'DRAW')], default='IN PRODUCTION', max_length=15),
        ),
    ]

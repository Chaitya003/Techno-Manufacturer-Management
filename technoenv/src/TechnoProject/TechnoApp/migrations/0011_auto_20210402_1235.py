# Generated by Django 3.1.4 on 2021-04-02 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TechnoApp', '0010_auto_20210402_1054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coil',
            name='coil_number',
            field=models.TextField(primary_key=True, serialize=False),
        ),
    ]

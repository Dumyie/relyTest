# Generated by Django 3.1.4 on 2020-12-07 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aml_assess', '0002_auto_20201207_0330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='pep',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='application',
            name='sanctioned',
            field=models.BooleanField(null=True),
        ),
    ]
# Generated by Django 3.1.4 on 2020-12-07 06:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('aml_assess', '0003_auto_20201207_0509'),
    ]

    operations = [
        migrations.CreateModel(
            name='PotentialMatch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check', models.CharField(max_length=255)),
                ('id_match', models.IntegerField()),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='aml_assess.application')),
            ],
        ),
    ]
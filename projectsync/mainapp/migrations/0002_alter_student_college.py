# Generated by Django 3.2.5 on 2023-09-22 17:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='college',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='mainapp.university'),
        ),
    ]

# Generated by Django 5.0.4 on 2024-08-08 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0016_alter_medicine_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medicine',
            name='instructions',
        ),
        migrations.AlterField(
            model_name='medicine',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]

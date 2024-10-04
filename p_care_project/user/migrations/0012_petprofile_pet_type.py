# Generated by Django 5.0.4 on 2024-06-26 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_petprofile_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='petprofile',
            name='pet_type',
            field=models.CharField(choices=[('dog', 'Dog'), ('cat', 'Cat'), ('bird', 'Bird')], default='Unknown', max_length=10),
            preserve_default=False,
        ),
    ]

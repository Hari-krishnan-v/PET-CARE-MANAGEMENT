# Generated by Django 5.0.4 on 2024-06-01 05:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_customer_email_confirmed_customer_otp_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='email_confirmed',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='otp',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='otp_created_at',
        ),
    ]

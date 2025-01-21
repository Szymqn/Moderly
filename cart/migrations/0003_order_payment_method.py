# Generated by Django 5.1.3 on 2025-01-21 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('credit_card', 'Credit Card'), ('paypal', 'PayPal')], default='credit_card', max_length=20),
        ),
    ]

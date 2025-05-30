# Generated by Django 5.1.7 on 2025-03-30 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_alter_user_email"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="average_transaction_amount",
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name="user",
            name="transaction_frequency",
            field=models.IntegerField(default=0),
        ),
    ]

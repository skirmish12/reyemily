# Generated by Django 4.2.2 on 2023-11-19 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posApp', '0008_alter_sales_total_qty'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='payment_method',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]

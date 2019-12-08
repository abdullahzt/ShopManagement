# Generated by Django 2.0.7 on 2019-12-08 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_management_main', '0005_auto_20191208_0644'),
    ]

    operations = [
        migrations.AddField(
            model_name='transactionday',
            name='sum',
            field=models.DecimalField(decimal_places=2, default=10, max_digits=12),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='quantity',
            field=models.DecimalField(decimal_places=1, max_digits=8),
        ),
    ]

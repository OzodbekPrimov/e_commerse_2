# Generated by Django 5.1.6 on 2025-03-01 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('pending', 'Kutilmoqda'), ('shipped', "Jo'natildi"), ('delivered', 'Yetkazildi')], db_index=True, default='pending', max_length=20),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(db_index=True, max_length=200),
        ),
    ]

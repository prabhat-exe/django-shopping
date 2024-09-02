# Generated by Django 5.0.4 on 2024-06-08 09:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.IntegerField(default=1)),
                ('cus_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.customers')),
            ],
        ),
    ]

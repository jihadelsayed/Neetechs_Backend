# Generated by Django 3.2.6 on 2021-08-06 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Checkout', '0003_remove_serviceorder_thread'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serviceorder',
            name='status',
            field=models.CharField(choices=[('requested', 'Requested'), ('confirmed', 'Confirmed'), ('canceled', 'Canceled'), ('pend', 'Pend'), ('payed', 'Payed')], default='requested', max_length=10, verbose_name='Status of service:'),
        ),
    ]

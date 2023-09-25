# Generated by Django 4.2.4 on 2023-09-05 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scanner', '0011_alter_coinstatscalculated_adx_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomePageSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timeframe', models.IntegerField(choices=[(5, '5m'), (15, '15m')], default=5)),
            ],
        ),
    ]
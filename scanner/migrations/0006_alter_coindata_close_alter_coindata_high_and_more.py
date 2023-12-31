# Generated by Django 4.2.4 on 2023-09-02 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scanner', '0005_alter_coindata_close_alter_coindata_high_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coindata',
            name='close',
            field=models.DecimalField(decimal_places=6, max_digits=20),
        ),
        migrations.AlterField(
            model_name='coindata',
            name='high',
            field=models.DecimalField(decimal_places=6, max_digits=20),
        ),
        migrations.AlterField(
            model_name='coindata',
            name='low',
            field=models.DecimalField(decimal_places=6, max_digits=20),
        ),
        migrations.AlterField(
            model_name='coindata',
            name='open',
            field=models.DecimalField(decimal_places=6, max_digits=20),
        ),
        migrations.AlterField(
            model_name='coindata',
            name='volume',
            field=models.DecimalField(decimal_places=4, max_digits=20),
        ),
    ]

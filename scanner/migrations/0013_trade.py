# Generated by Django 4.2.4 on 2023-09-05 15:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scanner', '0012_homepagesettings'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=6, max_digits=20)),
                ('coin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scanner.coin')),
            ],
        ),
    ]

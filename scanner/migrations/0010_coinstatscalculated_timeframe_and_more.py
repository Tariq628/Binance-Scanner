# Generated by Django 4.2.4 on 2023-09-04 20:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scanner', '0009_alter_coinstatscalculated_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='coinstatscalculated',
            name='timeframe',
            field=models.IntegerField(default=5),
        ),
        migrations.AddField(
            model_name='coinstatsrange',
            name='timeframe',
            field=models.IntegerField(default=5),
        ),
        migrations.AlterField(
            model_name='coinstatscalculated',
            name='coin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scanner.coin'),
        ),
        migrations.AlterField(
            model_name='coinstatsrange',
            name='coin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='scanner.coin'),
        ),
        migrations.AlterUniqueTogether(
            name='coinstatscalculated',
            unique_together={('coin', 'timeframe')},
        ),
        migrations.AlterUniqueTogether(
            name='coinstatsrange',
            unique_together={('coin', 'timeframe')},
        ),
    ]
# Generated by Django 2.0.7 on 2018-12-11 12:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('paymentapp', '0003_finance_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emp_data',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='paymentapp.Company'),
        ),
        migrations.AlterField(
            model_name='finance_data',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='paymentapp.Company'),
        ),
    ]

# Generated by Django 2.0.7 on 2018-12-28 11:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('paymentapp', '0012_auto_20181224_1734'),
    ]

    operations = [
        migrations.CreateModel(
            name='Emp_pay_slip',
            fields=[
                ('empid', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('empname', models.CharField(max_length=20)),
                ('basicpay', models.DecimalField(decimal_places=2, max_digits=8)),
                ('da', models.DecimalField(decimal_places=2, max_digits=8)),
                ('hra', models.DecimalField(decimal_places=2, max_digits=8)),
                ('pf', models.DecimalField(decimal_places=2, max_digits=8)),
                ('tax', models.DecimalField(decimal_places=2, max_digits=8)),
                ('pt', models.DecimalField(decimal_places=2, max_digits=8)),
                ('tsal', models.DecimalField(decimal_places=2, max_digits=8)),
                ('comapny', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='paymentapp.Company')),
            ],
        ),
        migrations.RemoveField(
            model_name='emp_pal_slip',
            name='comapny',
        ),
        migrations.AddField(
            model_name='emp_leaves',
            name='basic_pay',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.DeleteModel(
            name='Emp_pal_slip',
        ),
    ]
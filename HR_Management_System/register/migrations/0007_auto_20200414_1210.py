# Generated by Django 2.2.4 on 2020-04-14 03:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0006_auto_20200414_1207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeassignmenthistory',
            name='account_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='account_names3', to='register.AccountMaster'),
        ),
    ]

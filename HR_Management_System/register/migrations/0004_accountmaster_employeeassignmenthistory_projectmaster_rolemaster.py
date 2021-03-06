# Generated by Django 2.2.4 on 2020-04-14 02:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0003_employeestatus'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountMaster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_id', models.CharField(max_length=8, verbose_name='Account ID')),
                ('account_name', models.CharField(max_length=50, verbose_name='Account Name')),
                ('registered_date', models.DateField(blank=True, null=True, verbose_name='Registered Date')),
                ('active_status', models.CharField(choices=[('0', 'inactive'), ('1', 'active')], default='1', max_length=1, verbose_name='Active Status')),
            ],
        ),
        migrations.CreateModel(
            name='RoleMaster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role_id', models.CharField(max_length=8, verbose_name='Role ID')),
                ('role_description', models.CharField(max_length=50, verbose_name='Role Description')),
                ('role_name', models.CharField(max_length=50, verbose_name='Role Description')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectMaster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_id', models.CharField(max_length=8, verbose_name='Project ID')),
                ('project_name', models.CharField(max_length=50, verbose_name='Project Name')),
                ('registered_date', models.DateField(blank=True, null=True, verbose_name='Registered Date')),
                ('active_status', models.CharField(choices=[('0', 'inactive'), ('1', 'active')], default='1', max_length=1, verbose_name='Active Status')),
                ('account_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='account_ids2', to='register.AccountMaster')),
                ('account_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='account_names2', to='register.AccountMaster')),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeAssignmentHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(blank=True, null=True, verbose_name='Start Date')),
                ('end_date', models.DateField(blank=True, null=True, verbose_name='Start Date')),
                ('account_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='account_ids3', to='register.AccountMaster')),
                ('account_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='account_names3', to='register.AccountMaster')),
                ('employee_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employee_ids', to=settings.AUTH_USER_MODEL)),
                ('project_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_names', to='register.ProjectMaster')),
                ('project_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_ids', to='register.ProjectMaster')),
                ('role_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='role_ids', to='register.RoleMaster')),
                ('role_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='role_names', to='register.RoleMaster')),
            ],
        ),
    ]

# Generated by Django 5.0.3 on 2024-03-22 03:49

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_alter_scanresult_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='scanresult',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.CharField(max_length=100)),
                ('mac_address', models.CharField(max_length=50)),
                ('device_type', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('scan_result', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reports', to='main_app.scanresult')),
            ],
        ),
    ]
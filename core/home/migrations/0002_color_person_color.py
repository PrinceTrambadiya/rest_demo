# Generated by Django 5.0.2 on 2024-02-19 22:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='person',
            name='color',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='color', to='home.color'),
            preserve_default=False,
        ),
    ]
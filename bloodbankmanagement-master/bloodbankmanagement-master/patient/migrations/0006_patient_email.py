# Generated by Django 5.0.6 on 2024-08-17 23:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0005_alter_patient_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='Email',
            field=models.EmailField(default='example@example.com', max_length=254),
        ),
    ]

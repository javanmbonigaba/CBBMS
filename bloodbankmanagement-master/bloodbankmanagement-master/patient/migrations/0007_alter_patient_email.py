# Generated by Django 5.0.6 on 2024-08-17 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patient', '0006_patient_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='Email',
            field=models.EmailField(max_length=40),
        ),
    ]

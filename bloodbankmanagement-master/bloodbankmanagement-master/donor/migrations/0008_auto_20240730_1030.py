# Generated by Django 3.0.5 on 2024-07-30 08:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('donor', '0007_donor_email'),
    ]

    operations = [
        migrations.RenameField(
            model_name='donor',
            old_name='address',
            new_name='district',
        ),
    ]

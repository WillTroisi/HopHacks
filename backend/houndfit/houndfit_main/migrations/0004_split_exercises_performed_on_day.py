# Generated by Django 5.1.1 on 2024-09-14 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('houndfit_main', '0003_pastworkouts_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='split',
            name='exercises_performed_on_day',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]

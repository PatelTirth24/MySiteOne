# Generated by Django 3.2.4 on 2021-10-17 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderplaced',
            name='status',
            field=models.CharField(default='Pending', max_length=50),
        ),
    ]

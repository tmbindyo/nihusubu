# Generated by Django 5.0.3 on 2024-03-15 19:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0007_alter_state_latitude_alter_state_longitude'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='wikiDataId',
            field=models.CharField(max_length=50, null=True),
        ),
    ]

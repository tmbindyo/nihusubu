# Generated by Django 5.0.3 on 2024-03-15 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0008_alter_city_wikidataid'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalrole',
            name='is_active',
            field=models.BooleanField(default=False, help_text='Whether the group is active or not.', verbose_name='Is Active'),
        ),
    ]

# Generated by Django 5.0.6 on 2024-07-24 19:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codejam', '0004_area_remove_commonspace_name_commonspace_area'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='qty',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]

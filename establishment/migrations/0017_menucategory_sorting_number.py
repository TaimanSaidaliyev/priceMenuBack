# Generated by Django 4.2.11 on 2024-03-21 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('establishment', '0016_remove_menucategory_level_remove_menucategory_lft_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='menucategory',
            name='sorting_number',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Порядок сортировки'),
        ),
    ]

# Generated by Django 4.2.11 on 2024-03-23 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('establishment', '0017_menucategory_sorting_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='sorting_number',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Порядок сортировки'),
        ),
        migrations.AddField(
            model_name='products',
            name='sorting_number',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Порядок сортировки'),
        ),
    ]

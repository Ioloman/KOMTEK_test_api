# Generated by Django 3.2.4 on 2021-06-23 15:38

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Catalog',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='идентификатор')),
                ('name', models.CharField(max_length=150, verbose_name='наименование')),
                ('short_name', models.CharField(blank=True, max_length=50, verbose_name='короткое наименование')),
                ('description', models.TextField(blank=True, verbose_name='описание')),
                ('version', models.CharField(max_length=20, verbose_name='версия')),
                ('date', models.DateField(default=datetime.date.today, verbose_name='дата начала действия справочника этой версии')),
            ],
            options={
                'verbose_name': 'Справочник',
            },
        ),
        migrations.CreateModel(
            name='CatalogItem',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='идентификатор')),
                ('code', models.CharField(max_length=50, verbose_name='код элемента')),
                ('value', models.CharField(max_length=200, verbose_name='значение элемента')),
                ('catalog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.catalog', verbose_name='родительский идентификатор')),
            ],
            options={
                'verbose_name': 'Элемент справочника',
            },
        ),
        migrations.AddConstraint(
            model_name='catalog',
            constraint=models.UniqueConstraint(fields=('name', 'version'), name='unique_version'),
        ),
    ]

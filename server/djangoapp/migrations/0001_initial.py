# Generated by Django 5.2 on 2025-07-15 23:56

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CarMake',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True, primary_key=True, serialize=False,
                    verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='CarModel',
            fields=[
                ('id', models.BigAutoField(
                    auto_created=True, primary_key=True, serialize=False,
                    verbose_name='ID')),
                ('dealer_id', models.IntegerField()),
                ('name', models.CharField(max_length=100)),
                ('type', models.CharField(
                    choices=[
                        ('SEDAN', 'Sedan'), ('SUV', 'SUV'), ('WAGON', 'Wagon'),
                        ('HATCHBACK', 'Hatchback'), ('COUPE', 'Coupe'),
                        ('CONVERTIBLE', 'Convertible')
                    ], default='SUV', max_length=15)),
                ('year', models.IntegerField(
                    default=2023,
                    validators=[
                        django.core.validators.MaxValueValidator(2023),
                        django.core.validators.MinValueValidator(2015)
                    ])),
                ('car_make', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    to='djangoapp.carmake')),
            ],
        ),
    ]

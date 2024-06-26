# Generated by Django 5.0.2 on 2024-05-02 14:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('eadmin', '0001_initial'),
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='questions',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('examid', models.CharField(max_length=15)),
                ('qid', models.CharField(max_length=5, unique=True)),
                ('q', models.TextField(unique=True)),
                ('opta', models.TextField()),
                ('optb', models.TextField()),
                ('optc', models.TextField()),
                ('optd', models.TextField()),
                ('answer', models.TextField()),
            ],
            options={
                'unique_together': {('qid', 'examid')},
            },
        ),
        migrations.CreateModel(
            name='responses',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('examid', models.CharField(max_length=5)),
                ('studid', models.CharField(max_length=5)),
                ('reponse', models.CharField(max_length=500)),
                ('cor', models.CharField(max_length=2)),
                ('wrg', models.CharField(max_length=2)),
                ('una', models.CharField(max_length=2)),
                ('total', models.CharField(max_length=5)),
            ],
            options={
                'unique_together': {('studid', 'examid')},
            },
        ),
        migrations.CreateModel(
            name='Results',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('grade', models.CharField(max_length=10)),
                ('percentage', models.IntegerField(default=35)),
                ('marks', models.IntegerField(default=35)),
                ('examid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eadmin.exam')),
                ('reg_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.applicant')),
            ],
            options={
                'unique_together': {('examid', 'reg_no')},
            },
        ),
    ]

# Generated by Django 3.1.2 on 2020-10-12 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Table',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position_x', models.IntegerField()),
                ('position_y', models.IntegerField()),
                ('is_selected', models.BooleanField()),
                ('is_open', models.BooleanField()),
                ('name', models.TextField()),
            ],
        ),
    ]

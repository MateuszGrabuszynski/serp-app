# Generated by Django 2.2.3 on 2019-07-08 02:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('serp_app', '0005_auto_20190708_0410'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='result',
            options={'ordering': ('position',)},
        ),
    ]
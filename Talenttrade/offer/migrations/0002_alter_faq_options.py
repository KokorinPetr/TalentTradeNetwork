# Generated by Django 4.2.8 on 2023-12-28 19:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='faq',
            options={'ordering': ['-id']},
        ),
    ]

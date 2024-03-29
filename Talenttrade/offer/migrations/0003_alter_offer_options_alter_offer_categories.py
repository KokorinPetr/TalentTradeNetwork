# Generated by Django 4.2.8 on 2024-01-05 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0002_alter_faq_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='offer',
            options={'default_related_name': 'offers', 'ordering': ['-created_at']},
        ),
        migrations.AlterField(
            model_name='offer',
            name='categories',
            field=models.ManyToManyField(to='offer.category'),
        ),
    ]

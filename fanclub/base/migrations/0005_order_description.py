# Generated by Django 4.2.5 on 2023-10-15 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='description',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]

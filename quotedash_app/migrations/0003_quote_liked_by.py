# Generated by Django 2.2.4 on 2020-10-19 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quotedash_app', '0002_quote'),
    ]

    operations = [
        migrations.AddField(
            model_name='quote',
            name='liked_by',
            field=models.ManyToManyField(related_name='liked_quotes', to='quotedash_app.User'),
        ),
    ]

# Generated by Django 4.0.4 on 2022-04-29 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_token_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='token',
            name='title',
        ),
        migrations.AlterField(
            model_name='graph',
            name='folder',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterUniqueTogether(
            name='graph',
            unique_together={('name', 'token')},
        ),
    ]

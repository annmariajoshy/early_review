# Generated by Django 2.0 on 2019-04-18 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('early_review', '0003_auto_20190410_1214'),
    ]

    operations = [
        migrations.CreateModel(
            name='JsonFileUpload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('file_upload', models.FileField(upload_to='json_files')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]

# Generated by Django 4.0.3 on 2023-01-12 21:01

import Category.models
from django.db import migrations, models
import django.db.models.deletion
import imagekit.models.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ModelCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=896)),
                ('img', imagekit.models.fields.ProcessedImageField(blank=True, default='CategoryDefaultImage.jpg', upload_to=Category.models.cat_upload_location)),
                ('createdAt', models.DateTimeField(auto_now_add=True, verbose_name='date published')),
                ('updatedAt', models.DateTimeField(auto_now=True, verbose_name='date updated')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='Category.modelcategory')),
            ],
        ),
    ]

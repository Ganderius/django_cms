# Generated by Django 3.2.14 on 2022-07-12 09:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_blogblock_blog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogblock',
            name='blog',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='block', to='app.blog'),
        ),
    ]

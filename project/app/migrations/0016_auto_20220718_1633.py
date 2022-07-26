# Generated by Django 3.2.14 on 2022-07-18 13:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_auto_20220718_1536'),
    ]

    operations = [
        migrations.CreateModel(
            name='MenuSectionLinks',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('type', models.CharField(default='', max_length=7)),
                ('value', models.CharField(default='', max_length=255)),
                ('parentid', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MenuServices',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('type', models.CharField(default='', max_length=255)),
                ('value', models.CharField(default='', max_length=7)),
                ('parentId', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MenuServicesSections',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('parentid', models.IntegerField(null=True)),
                ('type', models.CharField(default='', max_length=7)),
                ('value', models.CharField(default='', max_length=255)),
                ('menu_services', models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.menuservices')),
            ],
        ),
        migrations.AddField(
            model_name='menu',
            name='parentid',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='menu',
            name='type',
            field=models.CharField(default='', max_length=7),
        ),
        migrations.AddField(
            model_name='menu',
            name='value',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.DeleteModel(
            name='MenuLink',
        ),
        migrations.AddField(
            model_name='menuservices',
            name='menu',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.menu'),
        ),
        migrations.AddField(
            model_name='menusectionlinks',
            name='menu_section',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.menuservicessections'),
        ),
    ]

# Generated by Django 3.2.14 on 2022-07-12 10:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20220712_1310'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='industriesblock',
            name='industry',
        ),
        migrations.CreateModel(
            name='IndustryType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('industry', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='type', to='app.industries')),
            ],
        ),
        migrations.AddField(
            model_name='industriesblock',
            name='industry_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='block', to='app.industrytype'),
        ),
    ]

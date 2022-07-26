# Generated by Django 3.2.14 on 2022-07-12 11:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20220712_1400'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogblock',
            name='blog',
            field=models.ForeignKey(default='1', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='block', to='app.blog'),
        ),
        migrations.AlterField(
            model_name='caseblock',
            name='case',
            field=models.ForeignKey(default='1', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='block', to='app.cases'),
        ),
        migrations.AlterField(
            model_name='clientblock',
            name='client',
            field=models.ForeignKey(default='1', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='block', to='app.clients'),
        ),
        migrations.AlterField(
            model_name='companiesblock',
            name='company',
            field=models.ForeignKey(default='1', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='block', to='app.companies'),
        ),
        migrations.AlterField(
            model_name='faqblock',
            name='faq',
            field=models.ForeignKey(default='1', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='block', to='app.faq'),
        ),
        migrations.AlterField(
            model_name='industrytype',
            name='industry',
            field=models.ForeignKey(default='1', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='type', to='app.industries'),
        ),
        migrations.AlterField(
            model_name='servicetype',
            name='service',
            field=models.ForeignKey(default='1', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='type', to='app.services'),
        ),
        migrations.AlterField(
            model_name='whyusblock',
            name='why_us',
            field=models.ForeignKey(default='1', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='block', to='app.whyus'),
        ),
    ]

# Generated by Django 4.0.3 on 2022-05-03 06:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_customuser_createdat_customuser_updatedat'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='category',
            field=models.IntegerField(choices=[(0, 'BUG反馈'), (1, '网站反馈'), (2, '其它')], default=0),
        ),
        migrations.AlterField(
            model_name='report',
            name='reportFeed',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.feed'),
        ),
        migrations.AlterField(
            model_name='report',
            name='reportReview',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.review'),
        ),
    ]
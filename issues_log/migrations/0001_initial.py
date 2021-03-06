# Generated by Django 1.9.2 on 2016-05-19 11:27

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('issues', '0003_service_i18n'),
    ]

    operations = [
        migrations.CreateModel(
            name='Issue_LogExtension',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_handler', models.CharField(blank=True, editable=False, max_length=128)),
                ('issue', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='log_ext', to='issues.Issue')),
            ],
            options={
                'verbose_name_plural': 'issue log extensions',
                'verbose_name': 'issue log extension',
                'db_table': 'issues_log_extension',
            },
        ),
        migrations.CreateModel(
            name='LogEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(db_index=True, default=django.utils.timezone.now)),
                ('status', models.CharField(choices=[('allocated', 'allocated'), ('handling', 'handling'), ('done', 'done')], max_length=32)),
                ('note', models.TextField(blank=True)),
                ('handler', models.CharField(blank=True, max_length=128)),
                ('attachment_url', models.URLField(blank=True)),
                ('issue', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='log_entries', to='issues.Issue')),
            ],
            options={
                'ordering': ('time',),
            },
        ),
    ]

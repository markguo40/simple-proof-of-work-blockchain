# Generated by Django 2.1.2 on 2018-10-20 14:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=100)),
                ('balance', models.DecimalField(decimal_places=18, default=0, max_digits=28)),
                ('current_nonce', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.TextField(default='')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('previous_hash', models.CharField(max_length=100)),
                ('nonce', models.BigIntegerField()),
                ('block_difficulty', models.IntegerField()),
                ('block_hash', models.CharField(blank=True, max_length=100)),
                ('block_producer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='server.Account')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=18, default=0, max_digits=28)),
                ('signature', models.BinaryField(max_length=1000000)),
                ('nonce', models.BigIntegerField()),
                ('transaction_hash', models.CharField(blank=True, max_length=100)),
                ('receiver', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='receive', to='server.Account')),
                ('sender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='send', to='server.Account')),
            ],
        ),
    ]
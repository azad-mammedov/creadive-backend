# Generated migration for refactoring ArrayField and JSONField usage
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        # Create new models
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('slug', models.SlugField(max_length=50, unique=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Technology',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('slug', models.SlugField(max_length=50, unique=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name_plural': 'Technologies',
            },
        ),
        migrations.CreateModel(
            name='ServiceFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('order', models.PositiveIntegerField(default=0)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_features', to='core.service')),
            ],
            options={
                'ordering': ['order', 'id'],
            },
        ),
        migrations.CreateModel(
            name='SocialLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('platform', models.CharField(choices=[('facebook', 'Facebook'), ('twitter', 'Twitter'), ('instagram', 'Instagram'), ('linkedin', 'LinkedIn'), ('github', 'GitHub'), ('youtube', 'YouTube'), ('website', 'Website'), ('other', 'Other')], max_length=20)),
                ('url', models.URLField(max_length=500)),
                ('order', models.PositiveIntegerField(default=0)),
                ('team_member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='social_links', to='core.teammember')),
            ],
            options={
                'ordering': ['order', 'id'],
            },
        ),
        
        # Remove old fields
        migrations.RemoveField(
            model_name='blogpost',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='portfolioitem',
            name='technologies',
        ),
        migrations.RemoveField(
            model_name='service',
            name='features',
        ),
        migrations.RemoveField(
            model_name='teammember',
            name='social',
        ),
        
        # Add new ManyToMany fields
        migrations.AddField(
            model_name='blogpost',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='blog_posts', to='core.tag'),
        ),
        migrations.AddField(
            model_name='portfolioitem',
            name='technologies',
            field=models.ManyToManyField(blank=True, related_name='portfolio_items', to='core.technology'),
        ),
        
        # Add unique constraints
        migrations.AlterUniqueTogether(
            name='servicefeature',
            unique_together={('service', 'name')},
        ),
        migrations.AlterUniqueTogether(
            name='sociallink',
            unique_together={('team_member', 'platform')},
        ),
    ]

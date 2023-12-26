# Generated by Django 4.2.8 on 2023-12-24 21:00

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_type', models.CharField(choices=[('DM', 'Dungeon Master'), ('Player', 'Player')], default='Player', max_length=10)),
                ('bio', models.CharField(max_length=355)),
                ('profile_image_url', models.URLField(max_length=255)),
                ('discord_username', models.CharField(max_length=55)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Ability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=25)),
                ('description', models.CharField(max_length=1555)),
            ],
        ),
        migrations.CreateModel(
            name='Alignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=55)),
                ('description', models.CharField(max_length=755)),
            ],
        ),
        migrations.CreateModel(
            name='Background',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=55)),
                ('description', models.CharField(max_length=3555)),
                ('languages_count', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='DnDClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=55)),
                ('description', models.CharField(max_length=1555)),
                ('hit_die', models.IntegerField()),
                ('primary_ability', models.CharField(max_length=35)),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=55)),
                ('description', models.CharField(max_length=755)),
                ('exotic', models.BooleanField(default=True)),
                ('typical_speakers', models.CharField(max_length=155)),
                ('script', models.CharField(max_length=35, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Race',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=35)),
                ('description', models.CharField(max_length=750)),
                ('speed', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='SavingThrow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=55)),
                ('description', models.CharField(max_length=355)),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=55)),
                ('description', models.CharField(max_length=2555)),
            ],
        ),
        migrations.CreateModel(
            name='Subclass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=55)),
                ('description', models.CharField(max_length=3555)),
                ('dndclass', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dungeonapi.dndclass')),
            ],
        ),
        migrations.CreateModel(
            name='PlayerUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lfg_status', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='player_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PersonalityTrait',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=75)),
                ('description', models.CharField(max_length=1555)),
                ('d8_number', models.IntegerField()),
                ('background', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dungeonapi.background')),
            ],
        ),
        migrations.CreateModel(
            name='Ideal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=75)),
                ('description', models.CharField(max_length=755)),
                ('alignment_group', models.CharField(max_length=35)),
                ('d6_number', models.IntegerField()),
                ('background', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dungeonapi.background')),
            ],
        ),
        migrations.CreateModel(
            name='Flaw',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=75)),
                ('description', models.CharField(max_length=1555)),
                ('d6_number', models.IntegerField()),
                ('background', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dungeonapi.background')),
            ],
        ),
        migrations.CreateModel(
            name='DungeonMasterUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lfg_status', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='dungeon_master_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='dndclass',
            name='saving_throw_prof_1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saving_throw_prof_1', to='dungeonapi.savingthrow'),
        ),
        migrations.AddField(
            model_name='dndclass',
            name='saving_throw_prof_2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saving_throw_prof_2', to='dungeonapi.savingthrow'),
        ),
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('character_name', models.CharField(max_length=55)),
                ('level', models.IntegerField()),
                ('sex', models.CharField(max_length=35)),
                ('bio', models.CharField(max_length=755)),
                ('notes', models.CharField(max_length=755)),
                ('character_appearance', models.CharField(max_length=755)),
                ('created_on', models.DateField(auto_now_add=True)),
                ('alignment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dungeonapi.alignment')),
                ('background', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dungeonapi.background')),
                ('player_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='player', to='dungeonapi.playeruser')),
                ('race', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dungeonapi.race')),
            ],
        ),
        migrations.CreateModel(
            name='Bond',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=75)),
                ('description', models.CharField(max_length=1555)),
                ('d6_number', models.IntegerField()),
                ('background', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dungeonapi.background')),
            ],
        ),
    ]

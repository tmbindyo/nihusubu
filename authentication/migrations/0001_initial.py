# Generated by Django 5.0.3 on 2024-03-15 17:18

import core.utils.validators
import django.contrib.auth.models
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
import pgcrypto.fields
import simple_history.models
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0013_group_created_at_group_deleted_at_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('iso3', models.CharField(max_length=3)),
                ('iso2', models.CharField(max_length=2)),
                ('numeric_code', models.CharField(max_length=3)),
                ('phone_code', models.CharField(max_length=5)),
                ('capital', models.CharField(max_length=255)),
                ('currency', models.CharField(max_length=3)),
                ('currency_name', models.CharField(max_length=255)),
                ('currency_symbol', models.CharField(max_length=5)),
                ('tld', models.CharField(max_length=5)),
                ('native', models.CharField(max_length=255)),
                ('nationality', models.CharField(max_length=255)),
                ('latitude', models.DecimalField(decimal_places=8, max_digits=10)),
                ('longitude', models.DecimalField(decimal_places=8, max_digits=11)),
                ('emoji', models.CharField(max_length=5)),
                ('emojiU', models.CharField(max_length=20)),
                ('translations', models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='InstitutionType',
            fields=[
                ('deletion_marker', models.IntegerField(blank=True, help_text='Soft-deletion marker.', null=True, verbose_name='Deletion Marker')),
                ('deleted_at', models.DateTimeField(blank=True, help_text='Date and time when record was marked as deleted.', null=True, verbose_name='Deleted At')),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, help_text='Date and time when record was created.', null=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Date and time when record was last updated.', null=True, verbose_name='Updated At')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Institution Type', max_length=70, verbose_name='Institution Type')),
            ],
            options={
                'verbose_name': 'Institution Type',
                'verbose_name_plural': 'Institution Types',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='InvalidResetAttempt',
            fields=[
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, help_text='Date and time when record was created.', null=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Date and time when record was last updated.', null=True, verbose_name='Updated At')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', pgcrypto.fields.EmailPGPSymmetricKeyField(editable=False, help_text='Email address used in sign-in attempt.', max_length=255, verbose_name='Email')),
            ],
            options={
                'verbose_name': 'Invalid Password Reset Attempt',
                'verbose_name_plural': 'Invalid Password Reset Attempts',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('translations', models.JSONField()),
                ('wikiDataId', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
            ],
            options={
                'verbose_name': 'Role',
                'verbose_name_plural': 'Roles',
                'ordering': ['name'],
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('auth.group', models.Model),
            managers=[
                ('objects', django.contrib.auth.models.GroupManager()),
            ],
        ),
        migrations.CreateModel(
            name='HistoricalInstitutionType',
            fields=[
                ('deletion_marker', models.IntegerField(blank=True, help_text='Soft-deletion marker.', null=True, verbose_name='Deletion Marker')),
                ('deleted_at', models.DateTimeField(blank=True, help_text='Date and time when record was marked as deleted.', null=True, verbose_name='Deleted At')),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, help_text='Date and time when record was created.', null=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(blank=True, editable=False, help_text='Date and time when record was last updated.', null=True, verbose_name='Updated At')),
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, verbose_name='ID')),
                ('name', models.CharField(help_text='Institution Type', max_length=70, verbose_name='Institution Type')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Institution Type',
                'verbose_name_plural': 'historical Institution Types',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('deletion_marker', models.IntegerField(blank=True, help_text='Soft-deletion marker.', null=True, verbose_name='Deletion Marker')),
                ('deleted_at', models.DateTimeField(blank=True, help_text='Date and time when record was marked as deleted.', null=True, verbose_name='Deleted At')),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, help_text='Date and time when record was created.', null=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(blank=True, editable=False, help_text='Date and time when record was last updated.', null=True, verbose_name='Updated At')),
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, verbose_name='ID')),
                ('first_name', pgcrypto.fields.CharPGPSymmetricKeyField(help_text='First name of user.', max_length=255, verbose_name='First Name')),
                ('middle_name', pgcrypto.fields.CharPGPSymmetricKeyField(blank=True, help_text='Middle name of user.', max_length=255, null=True, verbose_name='Middle Name')),
                ('last_name', pgcrypto.fields.CharPGPSymmetricKeyField(help_text='Last name of user.', max_length=255, verbose_name='Last Name')),
                ('email', pgcrypto.fields.EmailPGPSymmetricKeyField(db_index=True, error_messages={'unique': 'A user with the provided email already exists.'}, help_text='Email address of user.', max_length=255, validators=[django.core.validators.EmailValidator()], verbose_name='Email')),
                ('phone_number', pgcrypto.fields.CharPGPSymmetricKeyField(help_text='Phone number of user.', max_length=15, validators=[core.utils.validators.phone_number_model_validator], verbose_name='Phone Number')),
                ('is_active', models.BooleanField(default=False, help_text='Indicates whether user is active. Determines if user can sign in.', verbose_name='Is Active?')),
                ('is_staff', models.BooleanField(default=False, help_text='Indicates whether user can sign in to admin site.', verbose_name='Is Staff?')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Users',
                'verbose_name_plural': 'historical Userss',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('deletion_marker', models.IntegerField(blank=True, help_text='Soft-deletion marker.', null=True, verbose_name='Deletion Marker')),
                ('deleted_at', models.DateTimeField(blank=True, help_text='Date and time when record was marked as deleted.', null=True, verbose_name='Deleted At')),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, help_text='Date and time when record was created.', null=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Date and time when record was last updated.', null=True, verbose_name='Updated At')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of institution.', max_length=255, verbose_name='Institution Name')),
                ('physical_address', models.CharField(blank=True, help_text='Physical location of institution, such as building name, road name, etc.', max_length=255, null=True, verbose_name='Physical Address')),
                ('postal_address', models.CharField(blank=True, help_text='Postal address of insitution.', max_length=255, null=True, verbose_name='Postal Address')),
                ('phone_number', models.CharField(blank=True, help_text='Phone number of institution.', max_length=15, null=True, validators=[core.utils.validators.phone_number_model_validator], verbose_name='Phone Number')),
                ('email_address', models.CharField(blank=True, help_text='Email address of institution.', max_length=255, null=True, verbose_name='Email Address')),
                ('website', models.CharField(blank=True, help_text='Website of institution.', max_length=255, null=True, verbose_name='Email Address')),
                ('is_coordinating_institution', models.BooleanField(default=False, help_text='Indicates whether institution is a coordinator. Equivalent to superuser status.', verbose_name='Coordinating Institution?')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.country')),
                ('institution_type', models.ForeignKey(help_text='Type of institution.', on_delete=django.db.models.deletion.PROTECT, to='authentication.institutiontype')),
            ],
            options={
                'verbose_name': 'Institution',
                'verbose_name_plural': 'Institutions',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='HistoricalRole',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=150, verbose_name='name')),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, help_text='Date and time when record was created.', null=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(blank=True, help_text='Date and time when record was last updated.', null=True, verbose_name='Updated At')),
                ('deletion_marker', models.IntegerField(blank=True, help_text='Soft-deletion marker.,', null=True, verbose_name='Deletion Marker')),
                ('deleted_at', models.DateTimeField(blank=True, help_text='Date and time when record was marked as deleted.', null=True, verbose_name='Deleted At')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('institution', models.ForeignKey(blank=True, db_constraint=False, help_text='Institution associated with a role.', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='authentication.institution')),
            ],
            options={
                'verbose_name': 'historical Role',
                'verbose_name_plural': 'historical Roles',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalInstitution',
            fields=[
                ('deletion_marker', models.IntegerField(blank=True, help_text='Soft-deletion marker.', null=True, verbose_name='Deletion Marker')),
                ('deleted_at', models.DateTimeField(blank=True, help_text='Date and time when record was marked as deleted.', null=True, verbose_name='Deleted At')),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, help_text='Date and time when record was created.', null=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(blank=True, editable=False, help_text='Date and time when record was last updated.', null=True, verbose_name='Updated At')),
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of institution.', max_length=255, verbose_name='Institution Name')),
                ('physical_address', models.CharField(blank=True, help_text='Physical location of institution, such as building name, road name, etc.', max_length=255, null=True, verbose_name='Physical Address')),
                ('postal_address', models.CharField(blank=True, help_text='Postal address of insitution.', max_length=255, null=True, verbose_name='Postal Address')),
                ('phone_number', models.CharField(blank=True, help_text='Phone number of institution.', max_length=15, null=True, validators=[core.utils.validators.phone_number_model_validator], verbose_name='Phone Number')),
                ('email_address', models.CharField(blank=True, help_text='Email address of institution.', max_length=255, null=True, verbose_name='Email Address')),
                ('website', models.CharField(blank=True, help_text='Website of institution.', max_length=255, null=True, verbose_name='Email Address')),
                ('is_coordinating_institution', models.BooleanField(default=False, help_text='Indicates whether institution is a coordinator. Equivalent to superuser status.', verbose_name='Coordinating Institution?')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('country', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='authentication.country')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('institution_type', models.ForeignKey(blank=True, db_constraint=False, help_text='Type of institution.', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='authentication.institutiontype')),
            ],
            options={
                'verbose_name': 'historical Institution',
                'verbose_name_plural': 'historical Institutions',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.AddField(
            model_name='country',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.region'),
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('state_code', models.CharField(max_length=10)),
                ('type', models.CharField(blank=True, max_length=100, null=True)),
                ('latitude', models.DecimalField(decimal_places=8, max_digits=10)),
                ('longitude', models.DecimalField(decimal_places=8, max_digits=11)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.country')),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('latitude', models.DecimalField(decimal_places=8, max_digits=10)),
                ('longitude', models.DecimalField(decimal_places=8, max_digits=11)),
                ('wikiDataId', models.CharField(max_length=50)),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.state')),
            ],
        ),
        migrations.CreateModel(
            name='SubRegion',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('translations', models.JSONField()),
                ('wikiDataId', models.CharField(max_length=50)),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.region')),
            ],
        ),
        migrations.AddField(
            model_name='country',
            name='subregion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentication.subregion'),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('deletion_marker', models.IntegerField(blank=True, help_text='Soft-deletion marker.', null=True, verbose_name='Deletion Marker')),
                ('deleted_at', models.DateTimeField(blank=True, help_text='Date and time when record was marked as deleted.', null=True, verbose_name='Deleted At')),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, help_text='Date and time when record was created.', null=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Date and time when record was last updated.', null=True, verbose_name='Updated At')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', pgcrypto.fields.CharPGPSymmetricKeyField(help_text='First name of user.', max_length=255, verbose_name='First Name')),
                ('middle_name', pgcrypto.fields.CharPGPSymmetricKeyField(blank=True, help_text='Middle name of user.', max_length=255, null=True, verbose_name='Middle Name')),
                ('last_name', pgcrypto.fields.CharPGPSymmetricKeyField(help_text='Last name of user.', max_length=255, verbose_name='Last Name')),
                ('email', pgcrypto.fields.EmailPGPSymmetricKeyField(error_messages={'unique': 'A user with the provided email already exists.'}, help_text='Email address of user.', max_length=255, unique=True, validators=[django.core.validators.EmailValidator()], verbose_name='Email')),
                ('phone_number', pgcrypto.fields.CharPGPSymmetricKeyField(help_text='Phone number of user.', max_length=15, validators=[core.utils.validators.phone_number_model_validator], verbose_name='Phone Number')),
                ('is_active', models.BooleanField(default=False, help_text='Indicates whether user is active. Determines if user can sign in.', verbose_name='Is Active?')),
                ('is_staff', models.BooleanField(default=False, help_text='Indicates whether user can sign in to admin site.', verbose_name='Is Staff?')),
                ('groups', models.ManyToManyField(related_name='accounts_user_groups', to='auth.group')),
                ('user_permissions', models.ManyToManyField(related_name='accounts_user_permissions', to='auth.permission')),
            ],
            options={
                'verbose_name': 'Users',
                'ordering': ['first_name', 'last_name'],
            },
        ),
        migrations.CreateModel(
            name='PasswordResetToken',
            fields=[
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False, help_text='Date and time when record was created.', null=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Date and time when record was last updated.', null=True, verbose_name='Updated At')),
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', pgcrypto.fields.TextPGPSymmetricKeyField(editable=False, help_text='Password reset token issued.', verbose_name='Token')),
                ('expires_at', models.DateTimeField(editable=False, help_text='Expiration date and time of token.', verbose_name='Token Expires At')),
                ('used_at', models.DateTimeField(blank=True, editable=False, help_text='Date and time when token was used.', null=True, verbose_name='Token Used At')),
                ('user', models.ForeignKey(editable=False, help_text='User that generated reset token.', on_delete=django.db.models.deletion.PROTECT, to='authentication.user')),
            ],
            options={
                'verbose_name': 'Password Reset Token',
                'verbose_name_plural': 'Password Reset Tokens',
                'ordering': ['-created_at'],
            },
        ),
    ]
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

	dependencies = [
		('applications', '0002_alter_jobapplication_status'),
	]

	operations = [
		migrations.AlterField(
			model_name='jobapplication',
			name='date_applied',
			field=models.DateField(blank=True, default=django.utils.timezone.localdate, null=True),
		),
	]
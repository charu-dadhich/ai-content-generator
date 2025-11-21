# utils/migrations/0003_alter_classwisesubject_unique_together.py
from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0002_chapter_board_alter_servicetype_service_type'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],   # <-- do nothing in DB (avoids DROP)
            state_operations=[
                migrations.AlterUniqueTogether(
                    name='classwisesubject',
                    unique_together=set(),
                ),
            ],
        ),
    ]

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chat", "0002_auto_20210723_2200"),
    ]

    operations = [
        migrations.AddField( 
            model_name="thread",
            name="uuid",
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True),
        ),
        migrations.AddField(
            model_name="message",
            name="uuid",
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True, db_index=True),
        ),
    ]

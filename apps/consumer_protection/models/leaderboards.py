from apps.consumer_protection.models.users import Users
from django.db import models
from django.core.exceptions import ValidationError
from uuid import uuid4


class LeaderboardManager(models.Manager):
    def create(self, **all_fields):
        if not all_fields.get("producer"):
            raise ValidationError("producer cannot be blank")
        if not all_fields.get("score"):
            raise ValidationError("score cannot be blank")

        leaderboard = self.model(**all_fields)
        leaderboard.save(using=self._db)
        return leaderboard


class Leaderboard(models.Model):
    leaderboard_id = models.UUIDField(
        primary_key=True, default=uuid4, editable=False
    )
    producer_id = models.OneToOneField(
        Users, on_delete=models.PROTECT, related_name="leaderboard"
    )
    score = models.IntegerField(blank=False, null=False)

from django.db import models
from uuid import uuid4
from django.core.exceptions import ValidationError
from apps.consumer_protection.models.users import Users

ITEM_CATEGORIES = {"prodt": "product", "serve": "service"}


class ItemsManager(models.Manager):
    def create(self, **all_fields):
        if not all_fields.get("name"):
            raise ValidationError("name cannot be blank")
        if not all_fields.get("producer"):
            raise ValidationError("producer cannot be blank")
        if not all_fields.get("category"):
            raise ValidationError("category of product cannot be blank")
        item = self.model(**all_fields)
        item.save(using=self._db)
        return item


class Items(models.Model):

    item_id = models.UUIDField(
        default=uuid4, primary_key=True, editable=False
    )
    name = models.CharField(max_length=150, blank=False, null=False)
    producer_id = models.ForeignKey(
        Users, on_delete=models.PROTECT, related_name="items"
    )
    leaderboard_score = models.IntegerField(null=False, blank=True)
    category = models.CharField(
        choices=ITEM_CATEGORIES, blank=False, null=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ItemsManager()

    def __str__(self):
        return self.name

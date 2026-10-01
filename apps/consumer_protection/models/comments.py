from apps.consumer_protection.models.feedbacks import Feedbacks
from apps.consumer_protection.models.users import Users
from django.core.exceptions import ValidationError
from django.db import models
from uuid import uuid4


class CommentsManager(models.Manager):
    def create(self, **all_fields):
        if not all_fields.get("body"):
            raise ValidationError("body of content is required")
        if not all_fields.get("feedback_id"):
            raise ValidationError("feedback is required")
        if not all_fields.get("commenter_id"):
            raise ValidationError("commenter is required")

        comment = self.model(**all_fields)
        comment.save(using=self._db)
        return comment


class Comments(models.Model):

    comment_id = models.UUIDField(
        primary_key=True, default=uuid4, editable=False
    )
    body = models.TextField(blank=False, null=False)
    feedback_id = models.ForeignKey(
        Feedbacks, on_delete=models.CASCADE, related_name="comments"
    )
    commenter_id = models.ForeignKey(
        Users, on_delete=models.PROTECT, related_name="comments"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CommentsManager()

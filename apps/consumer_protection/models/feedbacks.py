from django.core.exceptions import ValidationError
from django.db import models
from uuid import uuid4
from apps.consumer_protection.models.items import Items
from apps.consumer_protection.models.users import Users


class FeedbacksManager(models.Manager):
    def create(self, **all_fields):
        if not all_fields.get("consumer_id"):
            raise ValidationError("consumer's id cannot be blank")
        if not all_fields.get("body"):
            raise ValidationError(
                "feedback cannot have a blank content"
            )
        if not all_fields.get("item_id"):
            raise ValidationError("item's id cannot be blank")

        feedback = self.model(**all_fields)
        feedback.save(using=self._db)
        return feedback


class Feedbacks(models.Model):
    feedback_id = models.UUIDField(
        primary_key=True, default=uuid4, editable=False
    )
    consumer_id = models.ForeignKey(
        Users, on_delete=models.PROTECT, related_name="feedbacks"
    )
    body = models.TextField(blank=False, null=False)
    item_id = models.ForeignKey(
        Items, on_delete=models.PROTECT, related_name="feedbacks"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = FeedbacksManager()

    def __str__(self):
        return self.created_at


class FeedbackResponseManager(models.Manager):
    def create(self, **all_fields):
        if not all_fields.get("responder_id"):
            raise ValidationError("responder is required")
        if not all_fields.get("feedback_id"):
            raise ValidationError("feedback is required")
        if not all_fields.get("body"):
            raise ValidationError("body of the content is required")

        response = self.model(**all_fields)
        response.save(using=self._db)
        return response


class FeedbackResponse(models.Model):
    feedback_response_id = models.UUIDField(
        primary_key=True, default=uuid4, editable=False
    )
    responder_id = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        related_name="feedback_responses",
    )
    feedback_id = models.OneToOneField(
        Feedbacks,
        on_delete=models.CASCADE,
        related_name="producer_response",
    )
    body = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = FeedbackResponseManager()


class FeedbackVerificationsManager(models.Manager):
    def create(self, **all_fields):
        if not all_fields.get("feedback_id"):
            raise ValidationError("feedback cannot be blank")
        # call ai to examine genuinety of the feedback, to obtain
        # the value for the genuinety status and pass it
        genuine = 1  # just for now
        feedback_verification = self.model(
            genuine=genuine, **all_fields
        )
        feedback_verification.save(using=self._db)
        return feedback_verification


class FeedbackVerifications(models.Model):

    class GenuineStatus(models.IntegerChoices):
        GENUINE = 1, "genuine"
        FAKE = 0, "fake"

    feedback_verification_id = models.UUIDField(
        primary_key=True, default=uuid4, editable=False
    )
    feedback_id = models.OneToOneField(
        Feedbacks, on_delete=models.CASCADE, related_name="verification"
    )
    genuine = models.IntegerField(choices=GenuineStatus.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = FeedbackVerificationsManager()

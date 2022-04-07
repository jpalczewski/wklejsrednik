"""Pastes models."""

# Standard Library
import secrets
from datetime import datetime, timedelta, timezone
from hashlib import md5

# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# 3rd-Party
from configurations import values

# Project
from users.models import User

SECRET_KEY = values.SecretValue(environ_name="SECRET_KEY", environ_prefix=None)
ATTACHMENT_TIMESPAN = values.IntegerValue(
    environ_name="ATTACHMENT_TIMESPAN", environ_prefix=None, default=300
)


class PasteBin(models.Model):
    """Pastebin model."""

    # Choices
    class ExpireChoices(models.TextChoices):
        # The first value is the actual value to be set
        # The second value is used for humans
        NEVER = 'NEVER', _('never')
        MIN = 'MIN', _('1 minute')
        HOUR = 'HOUR', _('1 hour')
        DAY = 'DAY', _('1 day')
        WEEK = 'WEEK', _('1 week')
        MONTH = 'MONTH', _('1 month')
        YEAR = 'YEAR', _('1 year')

    # Attributes
    title = models.CharField(_('title'), max_length=50)
    text = models.TextField(_('paste text'))
    date_of_creation = models.DateTimeField(_('date of creation'), blank=True)
    exposure = models.BooleanField(_('exposure'))
    expire_after = models.CharField(
        _('expire after'),
        max_length=5,
        choices=ExpireChoices.choices,
        default=ExpireChoices.NEVER,
    )
    date_of_expiry = models.DateTimeField(_('date of expiry'), null=True, blank=True)
    author = models.ForeignKey(
        User, verbose_name=_('author'), on_delete=models.CASCADE, null=True, blank=True
    )
    language = models.CharField(_('langauge'), max_length=50, default='Plain Text')
    attachment_token = models.CharField(
        _('token issued to upload attachments'),
        null=False,
        blank=False,
        max_length=32,
        db_index=True,
    )
    objects = models.Manager()

    # Static methods
    @staticmethod
    def get_time_choice(choice: str) -> timedelta:
        if choice == PasteBin.ExpireChoices.MIN:
            return timedelta(seconds=60)
        elif choice == PasteBin.ExpireChoices.HOUR:
            return timedelta(seconds=3600)
        elif choice == PasteBin.ExpireChoices.DAY:
            return timedelta(days=1)
        elif choice == PasteBin.ExpireChoices.WEEK:
            return timedelta(days=7)
        elif choice == PasteBin.ExpireChoices.MONTH:
            return timedelta(days=30)
        elif choice == PasteBin.ExpireChoices.YEAR:
            return timedelta(days=360)

    # Methods
    def save(self, *args, **kwargs):  # type: ignore
        if self.author is None:
            self.expire_after = 'WEEK'
        choice = self.expire_after
        self.date_of_creation = datetime.now().replace(tzinfo=timezone.utc)
        if choice == PasteBin.ExpireChoices.NEVER:
            self.date_of_expiry = None
        else:
            self.date_of_expiry = self.date_of_creation + PasteBin.get_time_choice(
                choice
            )
        self.attachment_token = secrets.token_hex(16)
        super().save(*args, **kwargs)

    def is_uploading_attachments_allowed(self) -> bool:
        upload_time_limit = self.date_of_creation + timedelta(
            seconds=ATTACHMENT_TIMESPAN
        )
        return datetime.now().replace(tzinfo=timezone.utc) < upload_time_limit

    # Special Methods
    def __str__(self) -> str:
        return f'{self.title}'

    # Meta
    class Meta:
        ordering = ['id']
        verbose_name = _('pastebin')
        verbose_name_plural = _('pastebins')


class Attachment(models.Model):
    def get_attachment_filename(self, filename: str) -> str:  #
        return 'attachments/{}/{}'.format(
            md5((str(SECRET_KEY) + str(self.paste.pk)).encode('utf-8')).hexdigest(),
            filename,
        )

    image = models.ImageField(upload_to=get_attachment_filename)
    paste = models.ForeignKey(
        PasteBin, on_delete=models.CASCADE, related_name='attachments'
    )

    def __str__(self) -> str:
        return f'{self.paste.title} - {self.image.name}'

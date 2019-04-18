from django.db import models
from .managers import UserProductReviewAfterSpamQuerySet, AuthUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy as _


class AbstractTimeStampModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True, editable=False)
    updated_on = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True


class UserProductReviewAfterSpam(AbstractTimeStampModel):
    """
    Model to add  UserProductReview details.
    """
    product_id = models.CharField(max_length=128)
    product_name = models.CharField(max_length=128)
    reviewer_id = models.CharField(max_length=128)
    reviewer_name = models.CharField(max_length=128)
    review_text = models.CharField(max_length=1000)
    overall_rating = models.DecimalField(max_digits=11, decimal_places=4, null=True)
    summary_product = models.CharField(max_length=500)
    timestamp_review = models.IntegerField(default=0, null=True, blank=True)
    date_review = models.DateField()

    objects = UserProductReviewAfterSpamQuerySet.as_manager()

    def __str__(self):
        return self.product_id


class AuthUser(AbstractBaseUser, PermissionsMixin):

    user_name = models.CharField(max_length=128, null=True, blank=True)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(_('staff status'), default=False)

    objects = AuthUserManager()

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['email']

    def __str__(self):
        return str(self.email)


class UserProductReviewAfterSpam(AbstractTimeStampModel):
    """
    Model to upload.
    """
    product_id = models.CharField(max_length=128)
    product_name = models.CharField(max_length=128)
    reviewer_id = models.CharField(max_length=128)
    reviewer_name = models.CharField(max_length=128)
    review_text = models.CharField(max_length=1000)
    overall_rating = models.DecimalField(max_digits=11, decimal_places=4, null=True)
    summary_product = models.CharField(max_length=500)
    timestamp_review = models.IntegerField(default=0, null=True, blank=True)
    date_review = models.DateField()

    objects = UserProductReviewAfterSpamQuerySet.as_manager()

    def __str__(self):
        return self.product_id



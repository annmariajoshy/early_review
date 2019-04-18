from django.conf.urls import url, include
from rest_framework import routers

from early_review.views import UserProductReviewAfterSpamViewSet, AuthUserViewSet, AuthUserModelViewSet, \
    FileUploadViewSet
from . import views

router = routers.SimpleRouter()
router.register('user-product-early', UserProductReviewAfterSpamViewSet,
                base_name='user-product-early')
router.register('registration', AuthUserViewSet,
                base_name='registration')
router.register('users', AuthUserModelViewSet,
                base_name='users')
router.register('file-upload', FileUploadViewSet, base_name='file-upload')

urlpatterns = [
    url(r'^api/', include(router.urls)),
]


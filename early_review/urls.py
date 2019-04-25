from django.conf.urls import url, include
from django.conf.urls.static import static
from rest_framework import routers
from early_review.views import UserProductReviewAfterSpamViewSet, AuthUserViewSet, AuthUserModelViewSet, \
    FileUploadViewSet
from early_review_backend import settings
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

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

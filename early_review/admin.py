from django.contrib import admin
from .models import UserProductReviewAfterSpam, AuthUser,JsonFileUpload,UserThreshold


admin.site.register(UserProductReviewAfterSpam)
admin.site.register(AuthUser)
admin.site.register(JsonFileUpload)
admin.site.register(UserThreshold)
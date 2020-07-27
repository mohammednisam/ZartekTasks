from django.contrib import admin
from post_app.models import TblPost,TblUserReview,TblUserPriority


# Register your models here.
admin.site.register(TblPost)
admin.site.register(TblUserReview)
admin.site.register(TblUserPriority)
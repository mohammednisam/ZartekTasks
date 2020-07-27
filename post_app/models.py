from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User as AuthUser
# Create your models here.

class TblPost(models.Model):

    vchr_caption = models.CharField(max_length=50, blank=True, null=True)
    txt_discription= models.TextField(blank=True, null=True)
    jsn_images = JSONField()
    dbl_tag1_weight = models.FloatField(blank=True, null=True)
    dbl_tag2_weight = models.FloatField(blank=True, null=True)
    dbl_tag3_weight = models.FloatField(blank=True, null=True)
    dat_created = models.DateField(blank=True, null=True)
    fk_created = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tbl_post'
    def __str__(self):
        return str(self.vchr_caption)


class TblUserReview(models.Model):

    fk_user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    fk_post = models.ForeignKey(TblPost, models.DO_NOTHING, blank=True, null=True)
    # bln_review = models.BooleanField(default=False)
    int_like = models.IntegerField(blank=True, null=True)
    int_dislike = models.IntegerField(blank=True, null=True)
    dat_review = models.DateField(blank=True, null=True)
    
    class Meta:
        managed = True
        db_table = 'tbl_user_review'
    def __str__(self):
        return str(self.fk_post__vchr_caption) + '-' + self.fk_user__frist_name+' '+ self.fk_user__last_name



class TblUserPriority(models.Model):

    fk_user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    dbl_total_tag1_weight = models.FloatField(blank=True, null=True)
    dbl_total_tag2_weight = models.FloatField(blank=True, null=True)
    dbl_total_tag3_weight = models.FloatField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'tbl_user_priority'
    def __str__(self):
        return self.fk_user__frist_name+' '+ self.fk_user__last_name



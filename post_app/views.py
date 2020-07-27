from django.contrib.auth.models import User

from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from datetime import datetime
from django.db.models import Q,Case,When,Value,CharField,FloatField,F,Max,BooleanField,Sum
from django.db.models.functions import Concat
from post_app.models import TblPost,TblUserReview,TblUserPriority
from rest_framework.parsers import MultiPartParser,FileUploadParser


class PostViewSets(ViewSet):
    """
    Viewset for add a post,list posts,like a post and view review of a particluar Post

    """
    def list(self, request):
        """
        list used to list all post with respect to user tag values and like value for user and admin respectively

        """
        try:
            lst_post_details=[]
            lst_sorted_posts = []
            # Details of all posts

            rst_post = list(TblPost.objects.values('vchr_caption','txt_discription','jsn_images','dbl_tag1_weight',\
                        'dbl_tag2_weight','dbl_tag3_weight','dat_created','fk_created__first_name',\
                            'fk_created__last_name','id'))
            dct_likes ={}
            dct_dislikes = {}
            if TblUserReview.objects.exists():
                # post and its total likes
                dct_likes = dict(TblUserReview.objects.values_list('fk_post_id').annotate(sum_like=Sum('int_like')))

                # post and its total dislikes
                dct_dislikes = dict(TblUserReview.objects.values_list('fk_post_id').annotate(sum_like=Sum('int_dislike')))
            
            if not rst_post:
                return Response({'status':'failed','message':'No Posts sdded'})
            
            if rst_post:
                for ins_post in rst_post:
                    dct_post = {}
                    dct_post['vchr_caption'] = ins_post['vchr_caption']
                    dct_post['txt_discription'] = ins_post['txt_discription']
                    dct_post['dbl_tag1_weight'] = ins_post['dbl_tag1_weight']
                    dct_post['dbl_tag2_weight'] = ins_post['dbl_tag2_weight']
                    dct_post['dbl_tag3_weight'] = ins_post['dbl_tag3_weight']
                    dct_post['dat_created'] = datetime.strftime(ins_post['dat_created'],'%d-%m-%Y ')
                    dct_post['vchr_creator'] = ins_post['fk_created__first_name'].title()+' '+ins_post['fk_created__last_name'].title() if ins_post['fk_created__last_name'] else ''
                    dct_post['txt_discription'] = ins_post['txt_discription']
                    dct_post['id'] = ins_post['id']
                    dct_post['int_like'] = dct_likes.get(ins_post['id'],0)
                    dct_post['int_dislike'] = dct_dislikes.get(ins_post['id'],0)
                    dct_post['lst_images'] = [settings.MEDIA_ROOT+'/'+str_image_path for str_image_path in ins_post['jsn_images']]
                    lst_post_details.append(dct_post)

            # Sort all the post with respect to their likes values for admin and user with out previous tagging value
            if request.user.is_staff or not TblUserReview.objects.filter(fk_user_id=request.user.id).exists():
                lst_sorted_posts = sorted(lst_post_details, key = lambda i: (i['int_like']),reverse=True)
            #  Sort the posts with respect to user taging value
            else:
                rst_user_prefrecnce =  TblUserPriority.objects.filter(fk_user_id=request.user.id).\
                                    values('dbl_total_tag1_weight','dbl_total_tag2_weight','dbl_total_tag3_weight').first()
                
                # sort the the tag value with thier values
                lst_orders = sorted(rst_user_prefrecnce.items(), key=lambda x: x[1], reverse=True)

                if rst_user_prefrecnce and lst_orders:
                    # Sort the posts with respect to sorted tag value
                    lst_sorted_posts = sorted(lst_post_details, key = lambda i: (i[lst_orders[0][0].replace('_total','')],i[lst_orders[1][0].replace('_total','')],i[lst_orders[2][0].replace('_total','')]),reverse=True)
            if lst_sorted_posts:
                return Response({'status':'sucess','data':lst_sorted_posts})

        except Exception  as e:
            return Response({'status':0,'message':str(e)})

    
    
    
    def create(self, request):
        """
        Create Post here

        """
        try:
            # Only Admin user (is_staff True user) are allowed to post
            if not request.user.is_staff:         
                return Response({'status':'Failed','message':'User don not have permission to post'})

            # Check there is a image in post.only post with images are allowed to post
            if request.FILES.getlist('postImage'):
                vchr_caption = request.data.get('vchrCaption')
                txt_discription= request.data.get('strDiscription')
                dbl_tag1_weight = request.data.get('fltTag1Weight')
                dbl_tag2_weight = request.data.get('fltTag2Weight')
                dbl_tag3_weight = request.data.get('fltTag3Weight')
                lst_post_image_path = []

                lst_post_image = request.FILES.getlist('postImage')
                for str_image in lst_post_image:
                    # Save the image user filesystemstorage
                    fs = FileSystemStorage(location=settings.MEDIA_ROOT)
                    vchr_bill_image = fs.save(str_image.name, str_image)
                    vchr_bill_image_path = fs.url(vchr_bill_image)
                    # append image name to list of image path
                    lst_post_image_path.append(vchr_bill_image_path.replace('/media/',''))

                ins_post = TblPost.objects.create(
                    vchr_caption=vchr_caption,
                    txt_discription=txt_discription,
                    jsn_images = lst_post_image_path,
                    dbl_tag1_weight=dbl_tag1_weight,
                    dbl_tag2_weight=dbl_tag2_weight,
                    dbl_tag3_weight=dbl_tag3_weight,
                    dat_created=datetime.now(),
                    fk_created = request.user
                )
                return Response({'status':'sucess','message':'Successfully Posted'})
            else:
                return Response({'status':'failed','message':'No Image Posted'})

        except Exception as e:
            return Response({'status':0,'message':str(e)})

    
    
    
    def retrieve(self, request, pk=None):
        """
        View Review Details of a particluar post

        """
        try:
            
            lst_post_review_details = list(TblUserReview.objects.filter(fk_post_id=pk).extra(select={'dat_reviewed':"to_char(tbl_user_review.dat_review, 'dd-mm-YYYY')",}).annotate(bln_like=Case(
                    When(int_like=1,then=Value(True)),
                    When(int_dislike=1 ,then=Value(False)),
                    output_field=BooleanField(),
                )).annotate(user_name=Concat('fk_user__first_name', Value(' '), 'fk_user__first_name')).values('user_name','dat_reviewed','bln_like'))
           
            if lst_post_review_details:
                return Response({'status':'sucess','data':lst_post_review_details})
            else:
                return Response({'status':'failed','message':'No User Reviewed this posted'})
        except Exception as e:
            return Response({'status':0,'message':str(e)})


            

    def update(self, request, pk=None):
        """
        
        Review a post here (Like/DisLike)

        """
        try:
            if not TblPost.objects.filter(id=pk).exists():
                return Response({'status':'failed','message':'Post not found'})

            if TblUserReview.objects.filter(fk_user=request.user,fk_post_id = pk).exists():
                return Response({'status':'failed','message':'Post Already Reviewed'})
            
            
            # save review details
            bln_review = True if request.data.get('blnReview').title()=='True' else False
            ins_review = TblUserReview.objects.create(
                fk_user=request.user,
                fk_post_id = pk,
                int_like = 1 if bln_review else 0,
                int_dislike = 1 if not bln_review else 0,
                dat_review = datetime.now()
            )
            ins_review.save()
            if bln_review: 
                # save user priority details for further post listing

                rst_post_tag_values = TblPost.objects.filter(id=pk).values('dbl_tag1_weight',\
                            'dbl_tag2_weight','dbl_tag3_weight').first()
                if TblUserPriority.objects.filter(fk_user=request.user).exists():
                    TblUserPriority.objects.filter(fk_user=request.user).update(
                        dbl_total_tag1_weight = F('dbl_total_tag1_weight') + rst_post_tag_values['dbl_tag1_weight'],
                        dbl_total_tag2_weight = F('dbl_total_tag2_weight') + rst_post_tag_values['dbl_tag2_weight'],
                        dbl_total_tag3_weight = F('dbl_total_tag3_weight') + rst_post_tag_values['dbl_tag3_weight']
                        )
                else:
                    ins_user_priority = TblUserPriority.objects.create(
                        fk_user=request.user,
                        dbl_total_tag1_weight = rst_post_tag_values['dbl_tag1_weight'],
                        dbl_total_tag2_weight = rst_post_tag_values['dbl_tag2_weight'],
                        dbl_total_tag3_weight = rst_post_tag_values['dbl_tag3_weight']
                    )
                    ins_user_priority.save()
            return Response({'status':'sucess'})

        except Exception as e:
            return Response({'status':0,'message':str(e)})
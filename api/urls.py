from django.urls import path
from api.views.bookApiView import *
from api.views.movieApiView import *
from api.views.groupApiView import *
from api.views.userApiView import *
from api.views.feedApiView import *
from api.views.reviewApiView import *
from api.views.groupAdminView import *
from .views import *
from .views.feedbackApiView import *
from .views.reportApiView import *
from .views.tagApiView import *


from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

'''
    path('group/deleteAdmin/<uuid:groupId>/<uuid:userId>',AdminDeleteView.as_view(),name="group_admin_remove"),
        # PUT : switch group main admin
    path('group/switchAdmin/<uuid:groupId>/<uuid:userId>',MainAdminSwitchView.as_view(),name="group_admin_switch"),
'''


urlpatterns = [
    # User Authentication 
    path('auth/register/', UserRegisterView.as_view(), name="register"),
    path('auth/activate/', UserActivateView.as_view(), name="email_activation"),
    path('auth/request/', RequestPasswordView.as_view(), name="email_verification"),
    path('auth/request-validate/', ResetPasswordTokenValidateView.as_view(), name="reset_password_validate"),
    path('auth/resetpwd/email/', ResetPasswordEmailView.as_view(), name="reset_password_email"),
    path('auth/resetpwd/old/', ResetPasswordbyOldpasswordView.as_view(), name="reset_password_oldpswd"),
    path('auth/requestquestion/', RequestQuestionView.as_view(), name="request_securityQuestion"),
    path('auth/resetpwd/question/', ResetPasswordbyQuestionView.as_view(), name="reset_password_secureQ"),
    path('auth/resetquestion/', ResetSecurityQuestionView.as_view(), name="reset_secureQ"),
    path('auth/login/', LoginView.as_view(), name="login"),
    path('auth/logout/', LogoutView.as_view(), name="logout"),


    # User Path
    path('user/<uuid:userId>', UserDetailView.as_view(), name="user_detail"),
    path('user/', UserCreateView.as_view(), name="user_create"),
    path('user/list', UserListView.as_view(), name="user_list"),

    # Books Path
    path('book/<uuid:bookId>', BookDetailView.as_view(), name="book_detail"),
    path('book/', BookCreateView.as_view(), name="book_create"),
    path('book/list', BookListView.as_view(), name="book_list"),
    path('book/react/<uuid:bookId>', BookReactionView.as_view(), name="book_reaction"),

    # Movies Path
    path('movie/<uuid:movieId>', MovieDetailView.as_view(), name="movie_detail"),
    path('movie/', MovieCreateView.as_view(), name="movie_create"),
    path('movie/list', MovieListView.as_view(), name="movie_list"),
    path('movie/react/<uuid:movieId>', MovieReactionView.as_view(), name="movie_reaction"),

    # Groups Path
        # GET: get a group detail by groupId
    path('group/<uuid:groupId>', GroupDetailView.as_view(), name="group_detail"),
        # GET:searh/list all group
    path('group/list', GroupListView.as_view(), name="group_list"),
        #POST:create group
    path('group/create', GroupCreateView.as_view(), name="group_create"),
        # POST : join group ; DELETE:leave group
    path('group/joinleave/<uuid:groupId>', JoinLeaveGroupView.as_view(), name="join_leave_group"),
        # GET:search/list all feed in group page
    path('group/feed/list/<uuid:groupId>',GroupFeedListView.as_view(),name="groupFeed_list"),
        # POST:create feed in group
    path('group/feed/create/<uuid:groupId>', GroupFeedCreateView.as_view(), name="groupFeed_create"),
        # POST : apply to become group admin
    path('group/admin/<uuid:groupId>', GroupAdminRequestView.as_view(), name="group_admin_apply"),
        # PUT : set group admin
    path('group/setRole/<uuid:groupId>/<uuid:userId>/<int:role>',SetRoleView.as_view(),name="group_set_role"),
        # PUT : Ban Member
    path('group/banMember/<uuid:groupId>/<uuid:userId>',GroupMemberBanView.as_view(),name="group_member_ban"),
        # GET : Show group user had joined
    path('group/joined',ShowUserGroupView.as_view(),name="group_user_join_list"),
        # GET : Sort by category
    path('group/category/<str:category>',GroupbyCategoryView.as_view(),name="group_category_list"),
        # GET : search/list all group member
    path('group/members/<uuid:groupId>',GroupMemberView.as_view(),name="group_member_list"),
        # GET : list all admin request
    path('group/request/<uuid:groupId>', ShowRequestView.as_view(), name="group_request_list"),
    path('group/requestuser/<uuid:groupId>', ShowRequestUserView.as_view(), name="group_requestuser_list"),
    path('group/setPin/<uuid:groupId>/<uuid:feedId>', SetPinFeedView.as_view(), name="pin_group_feed"),
    path('group/setFeatured/<uuid:groupId>/<uuid:feedId>', SetFeaturedFeedView.as_view(), name="featured_group_feed"),

    # Feed Path
    path('feed/<uuid:feedId>', FeedDetailView.as_view(), name="feed_detail"),
    path('feed/', FeedCreateView.as_view(), name="feed_create"),
    path('feed/list', FeedListView.as_view(), name="feed_list"),
    path('feed/react/<uuid:feedId>', FeedReactionView.as_view(), name="feed_reaction"),

    # Review Path
    path('review/<uuid:reviewId>', ReviewDetailView.as_view(), name="review_detail"),
    path('review/', ReviewCreateView.as_view(), name="review_create"),
    path('review/list', ReviewListView.as_view(), name="review_list"),
    path('review/react/<uuid:reviewId>', ReviewReactionView.as_view(), name="feed_reaction"),

    #Report Path
    path('report/<uuid:reportId>', ReportDetailView.as_view(), name="report_detail"),
    path('report/', ReportCreateView.as_view(), name="report_create"),
    path('report/list', ReportListView.as_view(), name="report_list"),
    
    # Feedback Path
    path('feedback/<uuid:feedbackId>', FeedbackDetailView.as_view(), name="feedback_detail"),
    path('feedback/', FeedbackCreateView.as_view(), name="feedback_create"),
    path('feedback/list', FeedbackListView.as_view(), name="feedback_list"),

    
    # path('auth/', obtain_auth_token),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verfy'), 

    #Tag Path
    path('tag/<uuid:tagId>', TagDetailView.as_view(), name="tag_detail"),
    path('tag/create/', TagCreateView.as_view(), name="create_tag"),
    path('tag/join/', TagJoinView.as_view(), name="join_tag"),
    path('tag/unjoin/<uuid:tagId>', TagUnjoinView.as_view(), name="unjoin_tag"),
    path('tag/list', TagListView.as_view(), name="tag_list"),
]
    
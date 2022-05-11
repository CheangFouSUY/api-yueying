from django.urls import path
from api.views.bookApiView import *
from api.views.movieApiView import *
from api.views.groupApiView import *
from api.views.userApiView import *
from api.views.feedApiView import *
from api.views.reviewApiView import *
from .views import *
from .views.feedbackApiView import *
from .views.reportApiView import *


from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)



urlpatterns = [
    # User Authentication 
    path('auth/register/', UserRegisterView.as_view(), name="register"),
    path('auth/activate/', UserActivateView.as_view(), name="email_activation"),
    path('auth/request/', RequestPasswordView.as_view(), name="email_verification"),
    path('auth/request-validate/', ResetPasswordTokenValidateView.as_view(), name="reset_password_validate"),
    path('auth/reset/', ResetPasswordView.as_view(), name="reset_password"),
    path('auth/login/', LoginView.as_view(), name="login"),
    path('auth/logout/', LogoutView.as_view(), name="logout"),
    
    # User Path
    path('user/<uuid:userId>', UserDetailView.as_view(), name="user_detail"),
    path('user/', UserListAndCreateView.as_view(), name="user_list_and_create"),

    # Books Path
    path('book/<uuid:bookId>', BookDetailView.as_view(), name="user_detail"),
    path('book/', BookListAndCreateView.as_view(), name="user_list_and_create"),

    # Movies Path
    path('movie/<uuid:movieId>', MovieDetailView.as_view(), name="movie_detail"),
    path('movie/', MovieListAndCreateView.as_view(), name="movie_list_and_create"),

    # Groups Path
        # GET: get a group detail by groupId
    path('group/<uuid:groupId>', GroupDetailView.as_view(), name="group_detail"),
        # GET:list all group ; POST:create group
    path('group/', GroupListAndCreateView.as_view(), name="group_list_and_create"),
        # POST : join group
    path('group/join/<uuid:groupId>', joinGroupView.as_view(), name="join_group"),
        # GET:list all feed ; POST:create feed in group
    path('group/feed/<uuid:groupId>',GroupFeedListAndCreateView.as_view(),name="groupFeed_list_and_create"),
        # POST : apply to become group admin
    path('group/admin/<uuid:groupId>',GroupAdminApplyView.as_view(),name="group_admin_apply"),
        # PUT : set group admin
    path('group/setAdmin/<uuid:groupId>/<uuid:userId>',AdminSetView.as_view(),name="group_admin_set"),
        # PUT : remove group admin
    path('group/deleteAdmin/<uuid:groupId>/<uuid:userId>',AdminDeleteView.as_view(),name="group_admin_remove"),
        # PUT : set pinned feed
    path('group/pinFeed/<uuid:groupId>/<uuid:feedId>',PinnedFeedView.as_view(),name="group_feed_pin"),
    path('group/unpinFeed/<uuid:groupId>/<uuid:feedId>',UnpinFeedView.as_view(),name="group_feed_unpin"),
        # PUT : set pinned feed
    path('group/featuredFeed/<uuid:groupId>/<uuid:feedId>',FeaturedFeedView.as_view(),name="group_feed_featured"),
    path('group/unfeaturedFeed/<uuid:groupId>/<uuid:feedId>',UnfeaturedFeedView.as_view(),name="group_feed_unfeatured"),
        # DELETE : Delete group feed
    path('group/delGFeed/<uuid:groupId>/<uuid:feedId>',GroupFeedDeleteView.as_view(),name="group_feed_delete"),
        # PUT : Ban Member
    path('group/banMember/<uuid:groupId>/<uuid:userId>',GroupMemberBanView.as_view(),name="group_member_ban"),

    # Feed Path
    path('feed/<uuid:feedId>', FeedDetailView.as_view(), name="feed_detail"),
    path('feed/', FeedListAndCreateView.as_view(), name="feed_list_and_create"),

    # Review Path
    path('review/<uuid:reviewId>', ReviewDetailView.as_view(), name="review_detail"),
    path('review/', ReviewListAndCreateView.as_view(), name="review_list_and_create"),

    #Report Path
    path('report/<uuid:reportId>', ReportDetailView.as_view(), name="report_detail"),
    path('report/', ReportListAndCreateView.as_view(), name="report_list_and_create"),

    # Feedback Path
    path('feedback/<uuid:feedbackId>', FeedbackDetailView.as_view(), name="feedback_detail"),
    path('feedback/', FeedbackListAndCreateView.as_view(), name="feedback_list_and_create"),

    
    # path('auth/', obtain_auth_token),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verfy'), 
]

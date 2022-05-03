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
    path('group/<uuid:groupId>', GroupDetailView.as_view(), name="group_detail"),
    path('group/', GroupListAndCreateView.as_view(), name="group_list_and_create"),

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

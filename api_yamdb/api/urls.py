from api.views import (CategoriesViewSet, CommentViewSet, GenresViewSet,
                       ReviewViewSet, TitleViewSet, UserViewSet, get_jwt_token,
                       register)
from django.urls import include, path
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(r"users", UserViewSet)
router.register(r'categories', CategoriesViewSet)
router.register(r'genres', GenresViewSet)
router.register(r'titles', TitleViewSet)
router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<reviews_id>\d+)/comments',
    CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', register, name='register'),
    path('v1/auth/token/', get_jwt_token, name='token'),
    path('v1/', include(router.urls)),
]

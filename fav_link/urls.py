from rest_framework import routers
from fav_link.views import FavoriteUrlViewSet, ManageTagViewSet, ManageCategoryViewSet

router = routers.DefaultRouter()
router.root_view_name = "favorite-urls"

router.register("urls", FavoriteUrlViewSet, basename="urls")
router.register("tags", ManageTagViewSet, basename="tags")
router.register("category", ManageCategoryViewSet, basename="category")

urlpatterns = router.urls

from rest_framework.routers import DefaultRouter
from library.views import BookCategoryViewSet,BookViewSet,ReaderViewSet,BorrowRecordViewSet

router = DefaultRouter()
router.register(r'book-categories', BookCategoryViewSet)
router.register(r'books', BookViewSet)
router.register(r'readers', ReaderViewSet)
router.register(r'borrows', BorrowRecordViewSet)
urlpatterns = router.urls
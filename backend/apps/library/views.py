from datetime import date

from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from backend.response import error_response, success_response
from library.models import Book, BookCategory, BorrowRecord, Reader
from library.serializers import (
    BookCategorySerializer,
    BookSerializer,
    BorrowRecordSerializer,
    ReaderSerializer,
)


def _query_text(params, key):
    value = params.get(key)
    if value is None:
        return ''
    return str(value).strip()


# 图书分类
class BookCategoryViewSet(ModelViewSet):
    queryset = BookCategory.objects.all()
    serializer_class = BookCategorySerializer
    search_fields = ['name']


# 图书
class BookViewSet(ModelViewSet):
    queryset = Book.objects.select_related('category').all()
    serializer_class = BookSerializer
    search_fields = ['name', 'author', 'publisher']

    def get_queryset(self):
        qs = super().get_queryset()
        name = _query_text(self.request.query_params, 'name')
        if name:
            qs = qs.filter(name__icontains=name)
        return qs


# 读者
class ReaderViewSet(ModelViewSet):
    queryset = Reader.objects.all()
    serializer_class = ReaderSerializer
    search_fields = ['name', 'phone']

    def get_queryset(self):
        qs = super().get_queryset()
        name = _query_text(self.request.query_params, 'name')
        if name:
            qs = qs.filter(name__icontains=name)
        return qs


# 借阅记录
class BorrowRecordViewSet(ModelViewSet):
    queryset = BorrowRecord.objects.select_related('reader', 'book').all()
    serializer_class = BorrowRecordSerializer
    http_method_names = ['get', 'post', 'head', 'options']

    def get_queryset(self):
        qs = super().get_queryset()
        params = self.request.query_params
        reader_name = _query_text(params, 'reader_name')
        book_name = _query_text(params, 'book_name')
        status = _query_text(params, 'status')
        if reader_name:
            qs = qs.filter(reader__name__icontains=reader_name)
        if book_name:
            qs = qs.filter(book__name__icontains=book_name)
        today = date.today()
        if status == 'returned':
            qs = qs.filter(return_date__isnull=False)
        elif status == 'borrowed':
            qs = qs.filter(return_date__isnull=True, due_date__gte=today)
        elif status == 'overdue':
            qs = qs.filter(return_date__isnull=True, due_date__lt=today)
        return qs

    @action(detail=True, methods=['post'], url_path='return')
    def return_book(self, request, pk=None):
        record = self.get_object()
        if record.return_date:
            return error_response('该记录已还书')
        record.return_date = date.today()
        record.save(update_fields=['return_date'])
        book = record.book
        book.remaining += 1
        book.save(update_fields=['remaining'])
        return success_response(self.get_serializer(record).data, message='还书成功')

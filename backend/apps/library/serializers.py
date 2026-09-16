from datetime import date, timedelta
from rest_framework import serializers
from library.models import Book, BookCategory, BorrowRecord, Reader


#图书分类序列化器
class BookCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCategory
        fields = ('id', 'name')
#图书序列化器
class BookSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Book
        fields = (
            'id', 'name', 'author', 'publisher',
            'category', 'category_name', 'inventory', 'remaining',
        )
#读者序列化器
class ReaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reader
        fields = ('id', 'name', 'gender', 'phone', 'max_borrow')
#借阅记录序列化器
class BorrowRecordSerializer(serializers.ModelSerializer):
    reader_name = serializers.CharField(source='reader.name', read_only=True)
    book_name = serializers.CharField(source='book.name', read_only=True)

    class Meta:
        model = BorrowRecord
        fields = (
            'id', 'reader', 'book', 'reader_name', 'book_name',
            'borrow_date', 'due_date', 'return_date',
        )
        read_only_fields = ('borrow_date', 'due_date', 'return_date')

    def validate(self, attrs):
        reader = attrs['reader']
        book = attrs['book']
        if book.remaining <= 0:
            raise serializers.ValidationError('该书已无剩余，无法借出')
        borrowed = reader.borrows.filter(return_date__isnull=True).count()
        if borrowed >= reader.max_borrow:
            raise serializers.ValidationError('该读者可借数量已用完')
        return attrs

    def create(self, validated_data):
        book = validated_data['book']
        book.remaining -= 1
        book.save(update_fields=['remaining'])
        validated_data['due_date'] = date.today() + timedelta(days=30)
        return super().create(validated_data)
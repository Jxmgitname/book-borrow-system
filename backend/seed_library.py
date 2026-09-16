"""写入截图用的演示数据。可重复执行：先清空业务表再插入。"""
import os
import sys
from datetime import date
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
sys.path.insert(0, str(BASE_DIR / 'apps'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

import django
django.setup()

from django.db import connection
from library.models import Book, BookCategory, BorrowRecord, Reader


def reset_auto_increment(table_name):
    with connection.cursor() as cursor:
        cursor.execute('ALTER TABLE %s AUTO_INCREMENT = 1' % table_name)


def seed():
    BorrowRecord.objects.all().delete()
    Book.objects.all().delete()
    Reader.objects.all().delete()
    BookCategory.objects.all().delete()
    reset_auto_increment('borrow_record')
    reset_auto_increment('book')
    reset_auto_increment('reader')
    reset_auto_increment('book_category')

    # 分类：按页面从上到下的顺序创建
    cat_names = ['文学小说', '计算机', '历史文化', '教育考试', '少儿读物', '经济管理', '自然科学', '艺术设计']
    cats = {name: BookCategory.objects.create(name=name) for name in cat_names}

    # 图书：先插后面的，列表按 id 倒序，常见书会排在上面
    book_rows = [
        ('设计中的设计', '原研哉', '山东人民出版社', '艺术设计', 8, 8),
        ('时间简史', '史蒂芬·霍金', '湖南科学技术出版社', '自然科学', 10, 10),
        ('经济学原理', '曼昆', '北京大学出版社', '经济管理', 12, 12),
        ('小王子', '圣埃克苏佩里', '人民文学出版社', '少儿读物', 20, 20),
        ('五年高考三年模拟', '曲一线', '教育科学出版社', '教育考试', 15, 15),
        ('明朝那些事儿', '当年明月', '北京联合出版公司', '历史文化', 18, 18),
        ('Python编程从入门到实践', '埃里克·马瑟斯', '人民邮电出版社', '计算机', 16, 16),
        ('平凡的世界', '路遥', '人民文学出版社', '文学小说', 14, 14),
        ('三体', '刘慈欣', '重庆出版社', '文学小说', 20, 20),
        ('活着', '余华', '作家出版社', '文学小说', 15, 15),
    ]
    books = {}
    for name, author, publisher, cat_name, inventory, remaining in book_rows:
        books[name] = Book.objects.create(
            name=name,
            author=author,
            publisher=publisher,
            category=cats[cat_name],
            inventory=inventory,
            remaining=remaining,
        )

    # 读者
    reader_rows = [
        ('吴芳', '女', '13900001008', 5),
        ('周杰', '男', '13900001007', 5),
        ('陈静', '女', '13700001006', 3),
        ('刘洋', '男', '13600001005', 5),
        ('赵敏', '女', '13500001004', 5),
        ('王强', '男', '13300001003', 5),
        ('李娜', '女', '13900001002', 5),
        ('张明', '男', '13800001001', 5),
    ]
    readers = {}
    for name, gender, phone, max_borrow in reader_rows:
        readers[name] = Reader.objects.create(
            name=name,
            gender=gender,
            phone=phone,
            max_borrow=max_borrow,
        )

    def add_borrow(reader_name, book_name, borrow_on, due_on, return_on=None):
        record = BorrowRecord(
            reader=readers[reader_name],
            book=books[book_name],
            due_date=due_on,
            return_date=return_on,
        )
        record.save()
        BorrowRecord.objects.filter(pk=record.pk).update(
            borrow_date=borrow_on,
            due_date=due_on,
            return_date=return_on,
        )

    # 借还：已还、借出中、已逾期都有，方便截状态标签
    add_borrow('陈静', '设计中的设计', date(2026, 8, 20), date(2026, 9, 19), date(2026, 9, 5))
    add_borrow('刘洋', '经济学原理', date(2026, 8, 1), date(2026, 8, 31), date(2026, 8, 18))
    add_borrow('吴芳', '五年高考三年模拟', date(2026, 9, 10), date(2026, 10, 10))
    add_borrow('周杰', '小王子', date(2026, 9, 8), date(2026, 10, 8))
    add_borrow('赵敏', '明朝那些事儿', date(2026, 9, 6), date(2026, 10, 6))
    add_borrow('王强', 'Python编程从入门到实践', date(2026, 9, 3), date(2026, 10, 3))
    add_borrow('李娜', '平凡的世界', date(2026, 9, 1), date(2026, 10, 1))
    add_borrow('张明', '三体', date(2026, 8, 28), date(2026, 9, 27))
    add_borrow('张明', '活着', date(2026, 7, 10), date(2026, 8, 9))  # 已逾期

    for book in Book.objects.all():
        out = book.borrows.filter(return_date__isnull=True).count()
        book.remaining = book.inventory - out
        book.save(update_fields=['remaining'])

    print('分类', BookCategory.objects.count())
    print('图书', Book.objects.count())
    print('读者', Reader.objects.count())
    print('借还', BorrowRecord.objects.count())


if __name__ == '__main__':
    seed()

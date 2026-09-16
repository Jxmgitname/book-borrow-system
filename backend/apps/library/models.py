from django.db import models#从 Django 的 db 模块里，拿出 models 这个工具包，不是类

#图书分类
class BookCategory(models.Model):#定义一个叫 BookCategory"图书分类“ 的类，并继承 models.Model
    name = models.CharField('分类名称', max_length=50, unique=True)#定义一个叫 name 的属性，类型为字符串，长度为 50，唯一且不为空

    class Meta:#定义一个叫 Meta 的类，用来描述这个类的一些元数据（metadata）
        db_table = 'book_category'#定义一个叫 db_table 的属性，值为 'book_category'
        verbose_name = '图书分类'#定义一个叫 verbose_name 的属性，值为 '图书分类'
        verbose_name_plural = verbose_name#定义一个叫 verbose_name_plural 的属性，值为 verbose_name
        ordering = ['id']#定义一个叫 ordering 的属性，值为 ['id']

    def __str__(self):#定义一个叫 __str__ 的函数，返回 name
        return self.name#返回 name
#图书表
class Book(models.Model):#定义一个叫 Book 的类，并继承 models.Model
    name = models.CharField('书名', max_length=50)
    author = models.CharField('作者', max_length=50)
    publisher = models.CharField('出版社', max_length=50, blank=True, default='')
    category = models.ForeignKey(
        BookCategory,
        on_delete=models.PROTECT,
        related_name='books',
        verbose_name='分类',
    )
    inventory = models.PositiveIntegerField('库存', default=0)
    remaining = models.PositiveIntegerField('剩余', default=0)

    class Meta:
        db_table = 'book'
        verbose_name = '图书'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return self.name
#读者表
class Reader(models.Model):
    GENDER_CHOICES = (
        ('男', '男'),
        ('女', '女'),
    )

    name = models.CharField('姓名', max_length=20)
    gender = models.CharField('性别', max_length=2, choices=GENDER_CHOICES, default='男')
    phone = models.CharField('电话', max_length=20, blank=True, default='')
    max_borrow = models.PositiveIntegerField('可借数量', default=5)

    class Meta:
        db_table = 'reader'
        verbose_name = '读者'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return self.name
#借阅记录表
class BorrowRecord(models.Model):#定义一个叫 BorrowRecord 的类，并继承 models.Model
    reader = models.ForeignKey(
        Reader,
        on_delete=models.PROTECT,
        related_name='borrows',
        verbose_name='读者',
    )
    book = models.ForeignKey(
        Book,
        on_delete=models.PROTECT,
        related_name='borrows',
        verbose_name='图书',
    )
    borrow_date = models.DateField('借书日期', auto_now_add=True)
    due_date = models.DateField('应还日期')
    return_date = models.DateField('还书日期', null=True, blank=True)

    class Meta:
        db_table = 'borrow_record'
        verbose_name = '借阅记录'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return f'{self.reader_id}-{self.book_id}'     
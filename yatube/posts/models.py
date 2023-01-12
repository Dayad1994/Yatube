from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


# Create your models here.
class Group(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    slug = models.CharField(max_length=10, verbose_name='Краткое название')

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = 'Группы'
        verbose_name = 'Группа'


class Post(models.Model):
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField('data published', auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='posts', verbose_name='Автор')
    group = models.ForeignKey(Group, blank=True, null=True,
                              on_delete=models.PROTECT, verbose_name='Группа')
    image = models.ImageField(upload_to='posts/', blank=True, null=True,
                              verbose_name='Картинка')

    class Meta:
        verbose_name_plural = 'Посты'
        verbose_name = 'Пост'
        ordering = ['-pub_date']


class Comment(models.Model):
    text = models.TextField(verbose_name='Текст')
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='comments', verbose_name='Пост')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='comments', verbose_name='Автор')
    created = models.DateTimeField('data published', auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Комментарии'
        verbose_name = 'Комментарий'
        ordering = ['-created']


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT,
                             related_name='follower', verbose_name='Подписчик')
    author = models.ForeignKey(User, on_delete=models.PROTECT,
                               related_name='following', verbose_name='Автор')

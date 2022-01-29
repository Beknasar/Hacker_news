from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.TextField(max_length=100, null=False, blank=False, verbose_name='Заголовок')
    link = models.URLField(max_length=200, verbose_name='Ссылка')
    date_create = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    vote_amount = models.IntegerField(default=0, verbose_name='Счетчик голосов')
    author=models.CharField(max_length=40, null=False, blank=False, default='Unknown', verbose_name='Author')

    def __str__(self):
        return f"{self.pk}. {self.title}"

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = "Статьи"
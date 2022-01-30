from django.db import models
from django.contrib.auth import get_user_model


class Post(models.Model):
    title = models.TextField(max_length=100, null=False, blank=False, verbose_name='Заголовок')
    link = models.URLField(max_length=200, verbose_name='Ссылка')
    date_create = models.DateField(auto_now_add=True, verbose_name='Дата создания')
    vote_amount = models.IntegerField(default=0, verbose_name='Счетчик голосов')
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_DEFAULT, default=1,
                               related_name='posts', verbose_name='Автор')

    def voted_by(self, user):
        votes = self.votes.filter(user=user)
        return votes.count() > 0

    def __str__(self):
        return f"{self.pk}. {self.title}"

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = "Статьи"


class PostVote(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                             related_name='article_likes', verbose_name='Пользователь')
    post = models.ForeignKey('webapp.Post', on_delete=models.CASCADE,
                                related_name='votes', verbose_name='Статья')

    def __str__(self):
        return f'{self.user.username} - {self.post.title}'

    class Meta:
        verbose_name = 'Голос за пост'
        verbose_name_plural = 'Голосы за посты'
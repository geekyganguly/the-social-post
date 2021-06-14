from django.db import models

from django.contrib.auth import get_user_model
User = get_user_model()


class Post(models.Model):
    content = models.TextField()
    picture = models.ImageField(upload_to='post_images', blank=True)
    likes = models.ManyToManyField(
        User, default=None, blank=True, related_name='likes')
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def __str__(self):
        return str(self.pk)

    def get_likes(self):
        return self.likes.all()

    def get_likes_count(self):
        return self.likes.all().count()

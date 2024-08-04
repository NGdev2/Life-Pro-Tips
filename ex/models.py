from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone

class CustomUser(AbstractUser):
    reputation = models.IntegerField(default=0)

    def can_downvote(self):
        return self.reputation >= 15 or self.is_superuser

    def can_delete_tips(self):
        return self.reputation >= 30 or self.is_superuser

    def update_reputation(self):
        reputation = 0
        for tip in self.tips.all():
            reputation += tip.upvotes.count() * 5
            reputation -= tip.downvotes.count() * 2
        self.reputation = max(reputation, 0)
        self.save()


class Tip(models.Model):
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tips')
    date = models.DateTimeField(default=timezone.now)
    upvotes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='upvoted_tips', blank=True)
    downvotes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='downvoted_tips', blank=True)

    def __str__(self):
        return f"{self.content} by {self.author}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.author.update_reputation()

    def delete(self, *args, **kwargs):
        author = self.author
        super().delete(*args, **kwargs)
        author.update_reputation()
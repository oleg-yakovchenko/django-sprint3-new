from django.db import models
from django.utils import timezone


class PostQuerySet(models.QuerySet):
    """QuerySet с методом для фильтрации опубликованных публикаций."""

    def published(self):
        return self.filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=timezone.now(),
        ).select_related('category', 'location', 'author')

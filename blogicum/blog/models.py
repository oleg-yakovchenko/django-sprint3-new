from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from .constants import (
    CATEGORY_STR_MAX_LENGTH,
    IS_PUBLISHED_HELP_TEXT,
    LOCATION_STR_MAX_LENGTH,
    NAME_MAX_LENGTH,
    POST_STR_MAX_LENGTH,
    PUB_DATE_HELP_TEXT,
    SLUG_HELP_TEXT,
)

User = get_user_model()


class PostQuerySet(models.QuerySet):
    """QuerySet с методом для фильтрации опубликованных публикаций."""

    def published(self):
        return self.filter(
            is_published=True,
            category__is_published=True,
            pub_date__lte=timezone.now(),
        )


class BaseModel(models.Model):
    """Абстрактная модель с общими полями."""

    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text=IS_PUBLISHED_HELP_TEXT,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено',
    )

    class Meta:
        abstract = True


class Category(BaseModel):
    title = models.CharField(
        max_length=NAME_MAX_LENGTH,
        verbose_name='Заголовок',
    )
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text=SLUG_HELP_TEXT,
    )

    class Meta(BaseModel.Meta):
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title[:CATEGORY_STR_MAX_LENGTH]


class Location(BaseModel):
    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
        verbose_name='Название места',
    )

    class Meta(BaseModel.Meta):
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self):
        return self.name[:LOCATION_STR_MAX_LENGTH]


class Post(BaseModel):
    objects = PostQuerySet.as_manager()

    title = models.CharField(
        max_length=NAME_MAX_LENGTH,
        verbose_name='Заголовок',
    )
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text=PUB_DATE_HELP_TEXT,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации',
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Местоположение',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория',
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ['-pub_date']

    def __str__(self):
        return self.title[:POST_STR_MAX_LENGTH]

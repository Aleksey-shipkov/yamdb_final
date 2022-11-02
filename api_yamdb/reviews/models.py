from django.db import models
from django.db.models import UniqueConstraint
from django.contrib.auth.models import AbstractUser
from django.db.models import Avg

from api_yamdb.settings import MY_PROFILE_URL_PATH
from reviews.validators import validate_year, validate_rating


class User(AbstractUser):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    USER_ROLES = (
        (ADMIN, ADMIN),
        (MODERATOR, MODERATOR),
        (USER, USER),
    )

    username = models.CharField(
        max_length=150,
        null=True,
        unique=True,
        verbose_name='Имя пользователя',
        help_text='Укажите имя пользователя'
    )
    email = models.EmailField(
        unique=True,
        max_length=254,
        verbose_name='Адрес электронной почты',
        help_text='Укажите адрес электронной почты'
    )
    first_name = models.CharField(
        max_length=150,
        null=True,
        verbose_name='Имя пользователя',
        help_text='Укажите имя'
    )
    last_name = models.CharField(
        max_length=150,
        null=True,
        verbose_name='Фамилия пользователя',
        help_text='Укажите фамилию'
    )
    bio = models.TextField(
        null=True,
        blank=True,
        verbose_name='О себе',
        help_text='О себе'
    )
    role = models.CharField(
        max_length=50,
        choices=USER_ROLES,
        default=USER,
        verbose_name='Роль',
        help_text='Укажите роль'
    )

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    class Meta:
        ordering = ('id',)
        constraints = (
            models.CheckConstraint(
                check=~models.Q(username__iexact=MY_PROFILE_URL_PATH),
                name='username_is_not_me'
            ),
        )
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Categories(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название',
        help_text='Введите название категории'
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='Slug категории',
        help_text='Укажите slug категории'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genres(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название',
        help_text='Введите название жанра'
    )
    slug = models.SlugField(
        unique=True,
        max_length=50,
        verbose_name='Slug жанра',
        help_text='Укажите slug жанра'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название',
        help_text='Введите название жанра'
    )
    year = models.PositiveSmallIntegerField(
        validators=(validate_year,),
        verbose_name='Дата выпуска',
        help_text='Введите дату выпуска'
    )
    description = models.CharField(
        max_length=400,
        blank=True,
        verbose_name='Описание',
        help_text='Укажите краткое описание группы'
    )
    genre = models.ManyToManyField(
        Genres,
        related_name='titles',
        verbose_name='Жанр',
        help_text='Жанр контента'
    )
    category = models.ForeignKey(
        Categories,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория',
        help_text='Категория контента'
    )
    rating = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        validators=(validate_rating,),
        verbose_name='Рейтинг',
        help_text='Рейтинг контента')

    def get_rating(self):
        rating_dict = Review.objects.filter(
            title__id=self.id).aggregate(Avg('score'))
        new_rating = rating_dict['score__avg']
        Title.objects.filter(id=self.id).update(rating=new_rating)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Контент'
        verbose_name_plural = 'Контент'


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Контент',
        help_text='Контент'
    )
    genre = models.ForeignKey(
        Genres,
        on_delete=models.CASCADE,
        verbose_name='Жанр',
        help_text='Жанр контента'
    )

    def __str__(self):
        return f'{self.title} - {self.genre}'

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Произведение - Жанр'
        verbose_name_plural = 'Произведение - Жанр'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
        help_text='Произведение отзыва'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор',
        help_text='Автор отзыва'
    )
    score = models.IntegerField(
        verbose_name='Оценка',
        help_text='Оценка отзыва'
    )
    text = models.TextField(
        verbose_name='Отзыв',
        help_text='Текст отзыва'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата отзыва',
        help_text='Дата написания отзыва'
    )

    class Meta:
        constraints = (
            UniqueConstraint(fields=('title', 'author',),
                             name='unique_reviews'
                             ),
        )
        ordering = ('-id',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text[:15]


class Comments(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
        help_text='Отзыв комментария'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
        help_text='Автор комментария'
    )
    text = models.TextField(
        verbose_name='Комментарий',
        help_text='Текст комментария'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата комментария',
        help_text='Дата написания комментария'
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:15]

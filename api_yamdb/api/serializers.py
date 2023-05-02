from datetime import date
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.relations import SlugRelatedField

from reviews.models import Review, Comment, Category, Genre, Title


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели категорий."""

    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели жанров."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра информации о произведениях."""

    rating = serializers.IntegerField(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для операций с произведениями."""

    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year',
                  'description', 'genre', 'category')
        validators = [
            UniqueTogetherValidator(
                queryset=Title.objects.all(),
                fields=('name', 'year'),
                message='Такое произведение уже существyет.'
            )
        ]

    def validate_year(self, value):
        if value > date.today().year:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего.')
        return value


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели отзывов."""

    author = SlugRelatedField(slug_field='username',
                              read_only=True)
    score = serializers.IntegerField(min_value=1, max_value=10)

    def validate(self, data):
        request = self.context.get('request')
        view = self.context.get('view')
        if (
            request.method != 'PATCH'
            and Review.objects.filter(
                author=request.user,
                title__id=view.kwargs.get('title_id')
            ).exists()
        ):
            raise serializers.ValidationError(
                'Вы уже оценили это произведение. '
                'Чтобы добавить новое мнение, '
                'дополните существующий отзыв.'
            )
        return data

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели комментариев."""

    author = SlugRelatedField(slug_field='username',
                              read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')

from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg
from rest_framework import viewsets, mixins
from rest_framework.filters import SearchFilter
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination

from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    TitleReadSerializer,
    ReviewSerializer,
    CommentSerializer
)
from .permissions import IsAdminAuthorOrReadOnly, IsAdminOrReadOnly
from .filters import TitleFilter
from reviews.models import Title, Review, Category, Genre


class CategoryGenreViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoryViewSet(CategoryGenreViewSet):
    """Вьюсет для эндпоинта Category."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CategoryGenreViewSet):
    """Вьюсет для эндпоинта Genre."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для эндпоинта Title."""

    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).order_by('id')
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TitleReadSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для эндпоинта Reviews."""

    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminAuthorOrReadOnly,)

    def get_queryset(self):
        """Все отзывы на произведение."""

        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        queryset = title.reviews.all()
        return queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для эндпоинта Comments."""

    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination
    permission_classes = (IsAdminAuthorOrReadOnly,)

    def get_queryset(self):
        """Все комментарии к отзыву."""

        review = get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title__id=self.kwargs.get('title_id')
        )
        queryset = review.comments.all()
        return queryset

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title__id=self.kwargs.get('title_id')
        )
        serializer.save(author=self.request.user, review=review)

from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import generics, permissions, mixins, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from . import models, serializers


class UserCreate(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.AllowAny]


class PostList(generics.ListCreateAPIView):
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def put(self, request, *args, **kwargs):
        post = models.Post.objects.filter(pk=kwargs['pk'], user=request.user)
        if post.exists():
            return self.update(request, *args, **kwargs)
        else:
            raise ValidationError(_("You cannot edit posts which are not yours!"))

    def delete(self, request, *args, **kwargs):
        post = models.Post.objects.filter(pk=kwargs['pk'], user=request.user)
        if post.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError(_("You cannot delete posts which are not yours!"))


class CommentList(generics.ListCreateAPIView):
    # queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        post = models.Post.objects.get(pk=self.kwargs['pk'])
        return models.Comment.objects.filter(post=post)

    def perform_create(self, serializer):
        post = models.Post.objects.get(pk=self.kwargs['pk'])
        serializer.save(user=self.request.user, post=post)


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def put(self, request, *args, **kwargs):
        comment = models.Comment.objects.filter(pk=kwargs['pk'], user=request.user)
        if comment.exists():
            return self.update(request, *args, **kwargs)
        else:
            raise ValidationError(_("You cannot edit comments which are not yours!"))

    def delete(self, request, *args, **kwargs):
        comment = models.Comment.objects.filter(pk=kwargs['pk'], user=request.user)
        if comment.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError(_("You cannot delete comments which are not yours!"))


class PostLikeCreate(generics.CreateAPIView, mixins.DestroyModelMixin):
    serializer_class = serializers.PostLikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        post = models.Post.objects.get(pk=self.kwargs['pk'])
        return models.PostLike.objects.filter(post=post, user=self.request.user)

    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError(_('You already like this post!'))
        post = models.Post.objects.get(pk=self.kwargs['pk'])
        return serializer.save(post=post, user=self.request.user)

    def delete(self, request, *args, **kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError(_("You don't like this post yet!"))

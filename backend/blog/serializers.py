from rest_framework import serializers
from .models import Post, User, Role, Tag
from django.db.models import Count
from django.db import IntegrityError
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
)


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ["id", "description"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["slug", "name"]


class TagFollowingSerializer(serializers.ModelSerializer):
    is_following = serializers.SerializerMethodField()
    follower_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Tag
        fields = ["slug", "name", "is_following", "follower_count"]

    def get_is_following(self, obj):
        user = self.context["request"].user
        if user.is_authenticated:
            return user in obj.followers.all()
        return False


class CookieTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = None

    def validate(self, attrs):
        attrs["refresh"] = self.context["request"].COOKIES.get("refresh_token")
        if attrs["refresh"]:
            return super().validate(attrs)
        else:
            raise InvalidToken(
                "No valid token found in cookie 'refresh_token'"
            )


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    default_error_messages = {
        "no_active_account": "Credenciales inválidas. Por favor, verifica tu correo electrónico y contraseña."
    }
    username_field = "email"


class UserShortSerializer(serializers.ModelSerializer):
    role = RoleSerializer()
    is_following = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "fullname",
            "profile_image",
            "initials",
            "role",
            "is_following"
        ]

    def get_is_following(self, obj):
        user = self.context["request"].user
        if user.is_authenticated:
            return user.following.filter(id=obj.id).exists()
        return False


class PostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    author = UserShortSerializer(read_only=True)
    is_boosted = serializers.SerializerMethodField(read_only=True)
    is_bookmarked = serializers.SerializerMethodField(read_only=True)
    is_author = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "subtitle",
            "content",
            "excerpt",
            "published",
            "updated_at",
            "boosts_count",
            "thumbnail",
            "tags",
            "status",
            "slug",
            "author",
            "is_boosted",
            "is_bookmarked",
            "is_author",
        ]

    def get_is_boosted(self, obj):
        user = self.context["request"].user
        if user.is_authenticated:
            return user.boosted_posts.filter(id=obj.id).exists()
        return False

    def get_is_bookmarked(self, obj):
        user = self.context["request"].user
        if user.is_authenticated:
            return user.bookmarks.filter(id=obj.id).exists()
        return False

    def get_is_author(self, obj):
        user = self.context["request"].user
        if user.is_authenticated:
            return obj.author == user
        return False


class PostAuthorSerializer(serializers.ModelSerializer):
    author = UserShortSerializer()
    popular_tag = serializers.SerializerMethodField()
    is_bookmarked = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "subtitle",
            "excerpt",
            "published",
            "thumbnail",
            "status",
            "slug",
            "author",
            "popular_tag",
            "is_bookmarked",
        ]

    def get_unique_slug(self, obj):
        return f"{obj.slug}-{obj.id}"

    def get_popular_tag(self, obj):
        most_common_tag = (
            obj.tags.annotate(
                tag_count=Count("slug")
            ).order_by("-tag_count").first()
        )
        if most_common_tag:
            tag_serializer = TagSerializer(most_common_tag)
            return tag_serializer.data
        else:
            return None

    def get_is_bookmarked(self, obj):
        user = self.context["request"].user
        if user.is_authenticated:
            return user.bookmarks.filter(id=obj.id).exists()
        return False


class PostListSerializer(serializers.ModelSerializer):
    popular_tag = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "subtitle",
            "excerpt",
            "published",
            "thumbnail",
            "status",
            "slug",
            "popular_tag",
        ]

    def get_popular_tag(self, obj):
        most_common_tag = (
            obj.tags.annotate(
                tag_count=Count("slug")
            ).order_by("-tag_count").first()
        )
        if most_common_tag:
            tag_serializer = TagSerializer(most_common_tag)
            return tag_serializer.data
        else:
            return None


class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)
    role_id = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(), source="role", write_only=True
    )
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "fullname",
            "firstName",
            "lastName",
            "initials",
            "email",
            "profile_image",
            "password",
            "role",
            "role_id",
        ]
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        role_id = validated_data.pop("role_id", None)
        password = validated_data.pop("password", None)
        user = self.Meta.model(**validated_data)
        if role_id:
            user.role_id = role_id
        if password:
            user.set_password(password)
        try:
            user.save()
        except IntegrityError:
            raise serializers.ValidationError(
                {
                    "email": [
                        "El usuario con este correo electrónico ya existe."
                    ]
                }
            )
        return user


class TagDetailSerializer(serializers.ModelSerializer):
    follower_count = serializers.IntegerField(read_only=True)
    post_count = serializers.IntegerField(read_only=True)
    is_following = serializers.SerializerMethodField()
    posts = PostAuthorSerializer(
        many=True, read_only=True
    )  # Campo de relación para los posts

    class Meta:
        model = Tag
        fields = [
            "slug",
            "name",
            "follower_count",
            "post_count",
            "is_following",
            "posts",
        ]

    def get_is_following(self, obj):

        request = self.context["request"]

        if request.user.is_authenticated:
            return request.user in obj.followers.all()
        return False

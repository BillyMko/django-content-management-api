from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Category, Tag, Content, ContentView
User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required = True)
    email = serializers.CharField(required = True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(
                                        username=validated_data['username'],
                                        password=validated_data['password'],
                                        email=validated_data['email']
                                        )

        return user
    
class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "description"]

        read_only_fields = ["id", "slug"]

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ["id", "name", "slug"]
        read_only_fields = ["id" ,"slug"]

class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name"]

class ContentListSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Content
        fields = ["id", "title", "difficulty", "author", "category", "tags", "slug", "created_at"]

class ContentDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = Content
        fields = ["id",
                  "title",
                  "difficulty",
                  "author",
                  "category",
                  "tags",
                  "slug",
                  "created_at",
                  "body",
                  "metadata",
                  "updated_at"
                  ]

class ContentCreateSerializer(serializers.ModelSerializer):   


    category_id = serializers.PrimaryKeyRelatedField(
            queryset = Category.objects.all(),
            source="category"
            )
        
    tags_id = serializers.PrimaryKeyRelatedField(
            queryset= Tag.objects.all(),
            source="tags",
            many=True,
            required= False
            )
        
    class Meta:
        model = Content
        fields= [
                    "title",
                    "body",
                    "category_id",
                    "tags_id",
                    "difficulty",
                    "metadata",
            ]
    
    def create(self, validated_data):
        tags = validated_data["tags"].pop()
        content = Content.objects.create(**validated_data)
        content.tags.set(tags)
        return content


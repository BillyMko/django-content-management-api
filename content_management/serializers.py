from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Category, Tag, Content, ContentView
User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required = True)
    email = serializers.CharField(required = True)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'role']

    def validate_role(self, value):
        if value == "admin":
            raise serializers.ValidationError("Admin accounts cannot be created through registration")
        return value

    def create(self, validated_data):

        if validated_data["role"] == "instructor":
            validated_data["status"]= "pending"
        
        else:
            validated_data["status"] = "approved"


        
        user = User.objects.create_user(
                                        username=validated_data['username'],
                                        password=validated_data['password'],
                                        email=validated_data['email'],
                                        role=validated_data['role'],
                                        status=validated_data['status']
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

    def validate_title(self, value):
        if len((value).strip()) < 10:
            raise serializers.ValidationError("Title must be at least 10 characters long")
        return value

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
            required= False,
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
        tags = validated_data.pop("tags", [])
        content = Content.objects.create(**validated_data)
        content.tags.set(tags)
        return content


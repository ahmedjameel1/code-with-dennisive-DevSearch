from rest_framework import serializers
from projects.models import Project, Tag, Review
from users.models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class TagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ProjectsSerializer(serializers.ModelSerializer):
    owner = ProfileSerializer(many=False)
    tags = TagsSerializer(many=True)
    reviews = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = '__all__'

    def get_reviews(self, obj):
        reviews = obj.review_set.all()
        serializer = ReviewsSerializer(reviews, many=True)
        return serializer.data
from rest_framework import serializers
from django.contrib.auth.models import User
from person.models import (UserProfile, TuitionClass, District, SubDistrict, Subject, Classes, SSC, HSC, HigherStudies, AfterHsc, Contact)
from posts.models import TuitionPost, BlogComment
from tolet.models import Post, PostFile, ToletComment



#person serializers
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        exclude = ['user']

class DistrictSerializer(serializers.ModelSerializer):
    class Meta:
        model = District
        fields = '__all__'

class SubDistrictSerializer(serializers.ModelSerializer):
    district=DistrictSerializer(many=False, read_only=True)
    class Meta:
        model = SubDistrict
        fields = '__all__'
        
class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class ClassesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classes
        fields = '__all__'
     
class TuitionClassSerializer(serializers.ModelSerializer):
    subject = SubjectSerializer(many=True, read_only=True)
    level = ClassesSerializer(many=True, read_only=True)
    district = DistrictSerializer(many=False, read_only=True)
    preferedPlace=SubDistrictSerializer(many=True, read_only=True)
    class Meta:
        model = TuitionClass
        exclude = ['user']

class SSCSerializer(serializers.ModelSerializer):
    class Meta:
        model = SSC
        exclude = ['user']

class HSCSerializer(serializers.ModelSerializer):
    class Meta:
        model = HSC
        exclude = ['user']

class AfterHscSerializer(serializers.ModelSerializer):
    class Meta:
        model = AfterHsc
        exclude = ['user']

class HigherStudiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = HigherStudies
        exclude = ['user']

class UserSerializer1(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [ 'username']


class UserSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer(many=False, read_only=True)
    ssc = SSCSerializer(many=False, read_only=True)
    hsc = HSCSerializer(many=False, read_only=True)
    afterhsc = AfterHscSerializer(many=False, read_only=True)
    higherstudies = HigherStudiesSerializer(many=False, read_only=True)
    tuitionclass = TuitionClassSerializer(many=False, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name',
                  'last_name', 'userprofile', 'ssc', 'hsc', 'afterhsc', 'higherstudies', 'tuitionclass']

#tuitionposts serializers


class BlogCommentSerializer(serializers.ModelSerializer):
    user=UserSerializer1(many=False, read_only=True)
    class Meta:
        model = BlogComment
        fields = '__all__'

class TuitionPostSerializer(serializers.ModelSerializer):
    comment = BlogCommentSerializer(many=True, read_only=True)
    preferedPlace=SubDistrictSerializer(many=True, read_only=True)
    class_in=ClassesSerializer(many=True, read_only=True)
    subject=SubjectSerializer(many=True, read_only=True)
    author=UserSerializer1(many=False, read_only=True)
    likes=UserSerializer1(many=True, read_only=True)
    views=UserSerializer1(many=True, read_only=True)
    class Meta:
        model = TuitionPost
        fields = '__all__'

#Toletposts serializers


class ToletCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer1(many=False, read_only=True)

    class Meta:
        model = ToletComment
        fields = '__all__'
class PostFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostFile
        fields = '__all__'
        
class PostSerializer(serializers.ModelSerializer):
    comment = ToletCommentSerializer(many=True, read_only=True)

    author = UserSerializer1(many=False, read_only=True)
    likes = UserSerializer1(many=True, read_only=True)
    views = UserSerializer1(many=True, read_only=True)

    class Meta:
        model = Post
        fields = '__all__'

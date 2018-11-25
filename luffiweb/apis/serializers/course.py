# Author: harry.cai
# DATE: 2018/11/5
from rest_framework import serializers
from apis import models


class CourseSerializer(serializers.ModelSerializer):
    level = serializers.CharField(source='course.get_level_display')

    class Meta:
        model = models.Course
        fields = ['id', 'title', 'course_img', 'level']


class CourseDetailSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='course.title')
    img = serializers.CharField(source='course.course_img')
    level = serializers.CharField(source='course.get_level_display')
    recommends = serializers.SerializerMethodField()
    chapter = serializers.SerializerMethodField()

    class Meta:
        model = models.CourseDetail
        fields = ['course', 'slogan', 'why', 'title', 'img', 'level', 'recommends', 'chapter']
        depth = 1

    def get_recommends(self, obj):
        # 获取推荐所有课程
        queryset = obj.recommend_courses.all()
        return [{'id': row.id, 'title': row.title} for row in queryset]

    def get_chapter(self, obj):
        # 获取所有章节
        queryset = obj.course.chapter_set.all()
        return [{'id': row.id, 'name': row.name} for row in queryset]


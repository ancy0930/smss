from rest_framework import serializers
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Student
        fields = ["user", "date_of_birth", "address"]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user = User.objects.create_user(**user_data)
        student = Student.objects.create(user=user, **validated_data)
        return student


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ["name"]


class GradeSerializer(serializers.ModelSerializer):
    student = StudentSerializer()
    subject = SubjectSerializer()

    class Meta:
        model = Grade
        fields = ["id", "student", "subject", "grade"]

    def create(self, validated_data):
        student_data = validated_data.pop("student")
        user_data = student_data.pop("user")
        user = User.objects.create_user(**user_data)
        student = Student.objects.create(user=user, **student_data)

        subject_data = validated_data.pop("subject")
        subject = Subject.objects.get_or_create(**subject_data)[0]

        grade = Grade.objects.create(student=student, subject=subject, **validated_data)
        return grade

    def validate_grade(self, value):
        allowed_grades = ["A", "B", "C", "D"]
        if value.upper() not in allowed_grades:
            raise serializers.ValidationError(
                "Grade must be one of 'A', 'B', 'C', or 'D'."
            )
        return value


class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = "__all__"


class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = ["name", "date"]


class ResultSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    exam = serializers.PrimaryKeyRelatedField(queryset=Exam.objects.all())

    class Meta:
        model = Result
        fields = ["id", "student", "exam", "score"]

    def create(self, validated_data):
        return Result.objects.create(**validated_data)

    def validate_score(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError("Score must be between 0 and 100.")
        return value


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = "__all__"


class ClassScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassSchedule
        fields = "__all__"


class ExamScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamSchedule
        fields = "__all__"


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"


class RoomAllocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomAllocation
        fields = "__all__"


class StaffAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StaffAssignment
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class CourseSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseSubject
        fields = "__all__"

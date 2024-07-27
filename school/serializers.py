from rest_framework import serializers
from .models import *


from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Ensure password is write-only

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username", "password"]

    def create(self, validated_data):
        # Extract password from validated data
        password = validated_data.pop("password")
        # Create user instance without saving to the database
        user = User(**validated_data)
        # Set password with proper hashing
        user.set_password(password)
        # Save the user instance
        user.save()
        return user


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()  # Nested serializer to include all User fields

    class Meta:
        model = Student
        fields = ["user", "date_of_birth", "address"]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user = User.objects.create_user(**user_data)
        student = Student.objects.create(user=user, **validated_data)
        return student

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["user_id"] = instance.user.id
        representation["username"] = instance.user.username
        return representation


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


from rest_framework import serializers
from .models import Exam


class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = ["id", "name", "date"]


class ResultSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    exam = ExamSerializer()  # Use ExamSerializer for output

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

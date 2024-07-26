from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"students", StudentViewSet)
router.register(r"enrollments", EnrollmentViewSet)
router.register(r"grades", GradeViewSet)
router.register(r"exams", ExamViewSet)
router.register(r"results", ResultViewSet)
router.register(r"attendances", AttendanceViewSet)
router.register(r"class-schedules", ClassScheduleViewSet)
router.register(r"exam-schedules", ExamScheduleViewSet)
router.register(r"rooms", RoomViewSet)
router.register(r"events", EventViewSet)
router.register(r"room-allocations", RoomAllocationViewSet)
router.register(r"staff-assignments", StaffAssignmentViewSet)
router.register(r"subjects", SubjectViewSet)
router.register(r"courses", CourseViewSet)
router.register(r"course-subjects", CourseSubjectViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

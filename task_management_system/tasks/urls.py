from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from .views import check_permission, ProjectViewSet, TaskViewSet, CommentViewSet, TagViewSet, AllTagsViewSet

# Create a router and register our ViewSets with it.
router = DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'all-tags', AllTagsViewSet, basename='all-tags')


projects_router = NestedDefaultRouter(router, r'projects', lookup='project')
projects_router.register(r'tasks', TaskViewSet, basename='project-tasks')


tasks_router = NestedDefaultRouter(projects_router, r'tasks', lookup='task')
tasks_router.register(r'comments', CommentViewSet, basename='task-comments')
tasks_router.register(r'tags', TagViewSet, basename='task-tags')


urlpatterns = [
    path('', include(router.urls)),
    path('', include(projects_router.urls)),
    path('', include(tasks_router.urls)),
    path('projects/<int:project_id>/check_permission/', check_permission, name='check-permission'),
]

from rest_framework import permissions
from .models import Project, Task, Comment, Tag


class IsProjectOwnerCheck(permissions.BasePermission):
   
    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner


class IsProjectOwner(permissions.BasePermission):
   
    def has_object_permission(self, request, view, obj):
        if view.action in ['create', 'update', 'partial_update', 'destroy']:
            project = obj.project if hasattr(obj, 'project') else None
            if project:
                return request.user == project.owner
        return True


class IsProjectOwnerOrMember(permissions.BasePermission):
 
    def has_object_permission(self, request, view, obj):
 
        if request.method in permissions.SAFE_METHODS:
            return self._is_owner_or_member(request.user, obj)

     
        if isinstance(obj, Project):
        
            is_owner = request.user == obj.owner
            return is_owner

        if isinstance(obj, Task):
    
            is_owner = request.user == obj.project.owner
            is_member = request.user in obj.project.members.all()
            return is_owner or is_member

        if isinstance(obj, Comment):
       
            is_owner = request.user == obj.task.project.owner
            is_member = request.user in obj.task.project.members.all()
            return is_owner or is_member

        if isinstance(obj, Tag):
           
            return self._can_view_and_modify_tag(request.user, obj)

        return False

    def _is_owner_or_member(self, user, obj):
        if isinstance(obj, Project):
            return user == obj.owner or user in obj.members.all()

        if isinstance(obj, Task):
            return user == obj.project.owner or user in obj.project.members.all()

        if isinstance(obj, Comment):
            return user == obj.task.project.owner or user in obj.task.project.members.all()

        if isinstance(obj, Tag):
            return self._can_view_and_modify_tag(user, obj)

        return False

    def _can_view_and_modify_tag(self, user, tag):
      
        for task in tag.tasks.all():
            if user == task.project.owner or user in task.project.members.all():
                return True

        return False

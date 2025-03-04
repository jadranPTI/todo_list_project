from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django_filters import rest_framework as filters
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.pagination import PageNumberPagination
from .serializers import TaskSerializer
from .models import Task

# ✅ Custom Pagination
class TaskPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data, completed_tasks, pending_tasks):
        return Response({
            "current_page": self.page.number,
            "total_pages": self.page.paginator.num_pages,
            "page_size": self.page_size,
            "total_items": self.page.paginator.count,
            "completed_tasks": completed_tasks,
            "pending_tasks": pending_tasks,
            "next": self.get_next_link(),
            "previous": self.get_previous_link(),
            "results": data
        })

# ✅ Custom Filter for Tasks
class TaskFilter(filters.FilterSet):
    class Meta:
        model = Task
        fields = {
            'title': ['icontains'],
            'category': ['icontains'],
            'completed': ['exact']
        }

# ✅ User Task View
class TaskListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user_tasks = Task.objects.filter(user=request.user)
            completed_tasks = user_tasks.filter(completed=True).count()
            pending_tasks = user_tasks.filter(completed=False).count()
            filtered_tasks = TaskFilter(request.GET, queryset=user_tasks).qs

            paginator = TaskPagination()
            paginated_tasks = paginator.paginate_queryset(filtered_tasks, request)
            serializer = TaskSerializer(paginated_tasks, many=True)

            return paginator.get_paginated_response(serializer.data, completed_tasks, pending_tasks)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            serializer = TaskSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ✅ Admin View
class AdminTaskListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        try:
            all_tasks = Task.objects.all()
            completed_tasks = all_tasks.filter(completed=True).count()
            pending_tasks = all_tasks.filter(completed=False).count()

            paginator = TaskPagination()
            paginated_tasks = paginator.paginate_queryset(all_tasks, request)
            serializer = TaskSerializer(paginated_tasks, many=True)

            return paginator.get_paginated_response(serializer.data, completed_tasks, pending_tasks)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# ✅ Task Update & Delete View
class TaskGetUpdateDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            task = get_object_or_404(Task, id=pk, user=request.user)
            serializer = TaskSerializer(task)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, pk):
        try:
            task = get_object_or_404(Task, id=pk, user=request.user)
            serializer = TaskSerializer(task, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        try:
            task = get_object_or_404(Task, id=pk, user=request.user)
            task.delete()
            return Response({"message": "Task deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

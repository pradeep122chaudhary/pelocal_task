from django.db import connection, transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from ..serializers import TaskSerializer
from ..init_db import dictfetchall, dictfetchone

TASK_COLUMNS = """
id, title, description, due_date, status, priority,
created_at, updated_at, completed_at, is_deleted
"""


class TaskListCreateAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        with connection.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT {TASK_COLUMNS}
                FROM tasks
                WHERE is_deleted = 0 AND created_by = %s
                ORDER BY created_at DESC
                """,
                [request.user.id]
            )
            rows = dictfetchall(cursor)

        return Response(TaskSerializer(rows, many=True).data)

    @transaction.atomic
    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO tasks
                (title, description, due_date, status, priority, created_by)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                [
                    data["title"],
                    data.get("description", ""),
                    data.get("due_date"),
                    data["status"],
                    data["priority"],
                    request.user.id,
                ]
            )

            cursor.execute(
                f"SELECT {TASK_COLUMNS} FROM tasks WHERE id = last_insert_rowid()"
            )
            task = dictfetchone(cursor)

        return Response(TaskSerializer(task).data, status=status.HTTP_201_CREATED)


class TaskDetailAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def _get_task(self, pk, user_id):
        with connection.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT {TASK_COLUMNS}
                FROM tasks
                WHERE id = %s AND created_by = %s AND is_deleted = 0
                """,
                [pk, user_id]
            )
            return dictfetchone(cursor)

    def patch(self, request, pk):
        if not self._get_task(pk, request.user.id):
            return Response({"detail": "Not found"}, status=404)

        serializer = TaskSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        updates, values = [], []
        for field in ("title", "description", "due_date", "status", "priority"):
            if field in serializer.validated_data:
                updates.append(f"{field} = %s")
                values.append(serializer.validated_data[field])

        values.extend([pk, request.user.id])

        with connection.cursor() as cursor:
            cursor.execute(
                f"""
                UPDATE tasks SET {', '.join(updates)}
                WHERE id = %s AND created_by = %s
                """,
                values
            )

        return Response({"message": "Updated"})

    def delete(self, request, pk):
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE tasks SET is_deleted = 1
                WHERE id = %s AND created_by = %s
                """,
                [pk, request.user.id]
            )
        return Response(status=204)

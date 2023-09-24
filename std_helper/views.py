from django.http import JsonResponse
from .models import Users, Lessons
from .serializers import UserSerializer, LessonSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .utils import sendMail


@api_view(["GET"])
def users(request):
    users = Users.objects.all()
    serializer = UserSerializer(users, many=True)
    return JsonResponse({"users": serializer.data}, safe=False)


@api_view(["POST"])
def create_user(request):
    try:
        user = Users.objects.get(mail=request.data["mail"])

        if user is not None and not user.is_active:
            print(user)
            sendMail([user.mail])
            return Response({"response": "Verification mail sended"}, status=status.HTTP_201_CREATED)

        return Response({"BAD_REQUEST": "user already exists"}, status=status.HTTP_400_BAD_REQUEST)
    except:
        pass

    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        sendMail([request.data["mail"]])
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response({"BAD_REQUEST": request.data}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def activate_account(request, mail):
    try:
        user = Users.objects.get(mail=mail)
        if user is None:
            return Response({"BAD_REQUEST": "given mail does not exist in database"}, status=status.HTTP_404_NOT_FOUND)

        user.is_active = True
        user.save()
        return Response({"response": "Account verified"})

    except Exception as e:
        print(e)


@api_view(["POST"])
def login_user(request):
    try:
        users = Users.objects.get(mail=request.data["mail"])
        if users is not None and not users.is_active:
            sendMail([users.mail])
            return Response({"users": UserSerializer(users).data}, status=status.HTTP_201_CREATED)
        return Response({"users": UserSerializer(users).data}, status=status.HTTP_200_OK)
    except:
        return Response({"BAD_REQUEST": request.data}, status=status.HTTP_404_NOT_FOUND)


@api_view(["GET"])
def lessons(request):
    lessons = Lessons.objects.all()
    serializer = LessonSerializer(lessons, many=True)
    return JsonResponse({"lessons": serializer.data}, safe=False)


@api_view(["POST"])
def create_lesson(request):
    serializer = LessonSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response({"BAD_REQUEST": request.data}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["DELETE"])
def delete_lesson(request, lesson):
    try:
        lesson = Lessons.objects.get(lesson_id=lesson)
        if lesson is not None:
            lesson.delete()
            return Response({"lesson_deleted": ""}, status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return Response({"BAD_REQUEST": e}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def set_meal_notify(request):
    user = Users.objects.get(mail=request.data["mail"])
    if user is not None:
        user.meal_notify = request.data["meal_notify"]
        user.save()
        return Response({"meal_updated": UserSerializer(user).data}, status=status.HTTP_201_CREATED)

    return Response({"BAD_REQUEST": request.data}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def user_lessons(request, user):
    try:
        lessons = Lessons.objects.filter(user=user)
        print(lessons)
        if lessons is not None:
            lessons_data = [
                {
                    "lessons_name": lesson.lessons_name,
                    "class_room": lesson.class_room,
                    "lesson_hour": lesson.lesson_hour,
                    "end_date": lesson.end_date,
                    "lesson_id": lesson.lesson_id,
                }
                for lesson in lessons
            ]
            return Response({"lessons": lessons_data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"BAD_REQUEST": ""}, status=status.HTTP_400_BAD_REQUEST)

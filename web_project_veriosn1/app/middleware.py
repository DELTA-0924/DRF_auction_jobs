from django.contrib.sessions.models import Session
from rest_framework.response import Response
from django.utils import timezone
class PreventLoginWithActiveSessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Если пользователь уже аутентифицирован, проверяем активные сессии
            active_sessions = Session.objects.filter(expire_date__gte=timezone.now(), user=request.user)
        
            if active_sessions.exists():
                # Есть активная сессия для этого пользователя, возвращаем ошибку или перенаправляем
                return Response({'error:':"Пользователь уже вошел в систему с другого устройства"})  # Замените 'error-page-url' на URL страницы ошибки или другую страницу
        
        # Продолжаем выполнение запроса
        response = self.get_response(request)
        return response   

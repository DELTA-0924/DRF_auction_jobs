from app.models import CustomUser  # Замените на имя вашей модели
results = CustomUser.objects.all()  # Выполнить запрос
print(results+"It's working!!!")  # Вывести результаты на консоль
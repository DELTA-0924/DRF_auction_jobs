from app.models import CustomUser  # �������� �� ��� ����� ������
results = CustomUser.objects.all()  # ��������� ������
print(results+"It's working!!!")  # ������� ���������� �� �������
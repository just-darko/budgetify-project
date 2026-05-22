from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics
from django.contrib.auth.models import User
from datetime import date
from .models import Category, Transaction, Goal, UpcomingPayment, BudgetLimit
from .serializers import CategorySerializer, TransactionSerializer, UserSerializer, GoalSerializer, UpcomingPaymentSerializer, BudgetLimitSerializer
from .serializers import RegisterSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer

    def get_queryset(self):
        # Pokazuj tylko transakcje zalogowanego użytkownika
        return Transaction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Przy zapisie automatycznie przypisz zalogowanego użytkownika
        serializer.save(user=self.request.user)

class GoalViewSet(viewsets.ModelViewSet):
    serializer_class = GoalSerializer

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UpcomingPaymentViewSet(viewsets.ModelViewSet):
    serializer_class = UpcomingPaymentSerializer

    def get_queryset(self):
        user = self.request.user
        today = date.today()

        # LOGIKA AUTOMATYZACJI:
        # Szukamy płatności, których data to dzisiaj lub przeszłość (<= today)
        overdue_payments = UpcomingPayment.objects.filter(user=user, date__lte=today)
        
        for payment in overdue_payments:
            # 1. Tworzymy z niej standardową transakcję
            Transaction.objects.create(
                user=user,
                category=payment.category,
                amount=payment.amount,
                date=payment.date,
                description=payment.name
            )
            # 2. Usuwamy ją z nadchodzących płatności
            payment.delete()

        # Zwracamy listę tych, które dopiero nadejdą (posortowane po dacie)
        return UpcomingPayment.objects.filter(user=user).order_by('date')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class BudgetLimitViewSet(viewsets.ModelViewSet):
    serializer_class = BudgetLimitSerializer

    def get_queryset(self):
        return BudgetLimit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,) # Pozwala na dostęp bez logowania
    serializer_class = RegisterSerializer
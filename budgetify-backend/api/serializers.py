from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Transaction, Goal, UpcomingPayment, BudgetLimit

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        # Zabraniamy wysyłania ID użytkownika z frontendu - ustawi go serwer
        read_only_fields = ['user']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        # Hasło tylko do zapisu
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
    
class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = '__all__'
        read_only_fields = ['user']

class UpcomingPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UpcomingPayment
        fields = '__all__'
        read_only_fields = ['user']

class BudgetLimitSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetLimit
        fields = '__all__'
        read_only_fields = ['user']

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        # Zabezpieczenie: hasło można tylko zapisać, nigdy odczytać przez API
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Używamy create_user, co automatycznie bezpiecznie "hashuje" (szyfruje) hasło!
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
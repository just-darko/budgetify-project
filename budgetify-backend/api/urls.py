from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView, CategoryViewSet, TransactionViewSet, GoalViewSet, UpcomingPaymentViewSet, BudgetLimitViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'transactions', TransactionViewSet, basename='transaction')
router.register(r'goals', GoalViewSet, basename='goal')
router.register(r'upcoming', UpcomingPaymentViewSet, basename='upcoming')
router.register(r'limits', BudgetLimitViewSet, basename='limit')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
]
from rest_framework import generics, permissions
from .serializers import AccountSerializer
from first_app.models import Account
from rest_framework.exceptions import ValidationError


class AccountsList(generics.ListAPIView):
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Account.objects.all()

class AccountsListCreate(generics.ListCreateAPIView):
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Account.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AccountRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Account.objects.all()

    def delete(self, request, *args, **kwargs):
        account = Account.objects.filter(pk=kwargs['pk'], user=self.request.user)
        if account.exists():
            return self.destroy(request, *args, **kwargs)
        else:
            raise ValidationError('Its not your post ._.')


from rest_framework.permissions import BasePermission

class EsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.rol and request.user.rol.nombre.lower() == 'admin'

class EsVendedor(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.rol and request.user.rol.nombre.lower() == 'vendedor'

class EsCliente(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.rol and request.user.rol.nombre.lower() == 'cliente'

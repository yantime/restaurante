from email import message
from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.request import Request

class soloAdminPuedeEscribir(BasePermission):
    message = 'Solo el administrador puede realizar esta accion'
    def has_permission(self, request:Request, view):
        print(request.user)
        print(request.user.nombre)
        print(request.user.rol)
        print(request.auth)

        if request.method in SAFE_METHODS:
            return True 
    
        else:
            return request.user.rol == 'admin'


class soloMozoPuedeEscribir(BasePermission):
    message = 'Solo el mozo puede realizar esta accion'
    def has_permission(self, request:Request, view):
        print(request.user)
        print(request.user.nombre)
        print(request.user.rol)
        print(request.auth)

        if request.method in SAFE_METHODS:
            return True 
    
        else:
            return request.user.rol == 'mozo'   
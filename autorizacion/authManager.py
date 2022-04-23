from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, correo, nombre, rol, password):
        if not correo: 
            raise ValueError('El usuario debe tener un correo')
        
        correo = self.normalize_email(correo)
        nuevo_usuario = self.model(correo=correo, nombre=nombre, rol=rol)
        nuevo_usuario.set_password(password)
        nuevo_usuario.save(using=self._db)
        return nuevo_usuario
    
    def create_superuser(self, correo, nombre, rol, password):
        usuario = self.create_user(correo, nombre, rol, password)
        usuario.is_staff = True
        usuario.is_superuser = True
        usuario.save(using=self._db)
        
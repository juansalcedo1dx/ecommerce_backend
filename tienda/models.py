from django.db import models

# Create your models here.
# tienda/models.py
# Re-exporta los modelos que están en submódulos para que Django los registre
# (no mover nada, sólo importar para que Django vea todas las clases Model).

# Usuarios
try:
    from .usuarios.models import *  # Usuario, RolUsuario, SeguridadUsuario, etc.
except Exception:
    # Import fallbacks por si hay errores de dependencias durante desarrollo
    pass

# Productos
try:
    from .productos.models import *
except Exception:
    pass

# Categorias
try:
    from .categorias.models import *
except Exception:
    pass

# Carritos
try:
    from .carritos.models import *
except Exception:
    pass

# Pedidos
try:
    from .pedidos.models import *
except Exception:
    pass

# Envios
try:
    from .envios.models import *
except Exception:
    pass

# Politicas
try:
    from .politicas.models import *
except Exception:
    pass

# Tenants y Tiendas (si están en subpaquetes)
try:
    from .tenants.models import *
except Exception:
    pass

try:
    from .tiendas.models import *
except Exception:
    pass

# Seguridad (modelos de auditoría, bloqueo, etc.)
try:
    from .seguridad.models import *
except Exception:
    pass

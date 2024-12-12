from django.db import models

# Create your models here.

class accesos(models.Model):
    usuario = models.CharField(max_length=200, blank=True, null=True)
    contrasenia = models.CharField(max_length=200, blank=True, null=True)
    class Meta:
        db_table = 'accesos'

class usuarios(models.Model):
    id_acceso = models.ForeignKey(accesos, on_delete=models.CASCADE)
    id_tipo_genero = models.ForeignKey('genero', on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    class Meta:
        db_table = 'usuarios'

class genero(models.Model):
    tipo_genero = models.CharField(max_length=200)
    class Meta:
        db_table = 'genero'


class archivos(models.Model):
    id_usuario = models.ForeignKey(usuarios, on_delete=models.CASCADE)
    id_tipo_archivo = models.ForeignKey('tipo_archivos', on_delete=models.CASCADE)
    id_carpeta = models.ForeignKey('carpetas', on_delete=models.CASCADE)
    nombre_archivo = models.CharField(max_length=100)
    fecha_guardado = models.DateField(blank=True, null=True)
    archivo = models.BinaryField(blank=True, null=True)
    tamanio = models.DecimalField(max_digits=12, decimal_places=2)
    class Meta:
        db_table = 'archivos'

class carpetas(models.Model):
    id_usuario = models.ForeignKey(usuarios, on_delete=models.CASCADE)
    id_carpeta_superior = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    nombre_carpeta = models.CharField(max_length=200, blank=True, null=True)
    fecha_creacion = models.DateField(blank=True, null=True)
    class Meta:
        db_table = 'carpetas'

class tipo_archivos(models.Model):
    tipo_archivo = models.CharField(max_length=200)
    class Meta:
        db_table = 'tipos_archivos'

class permisos(models.Model):
    tipo_permiso = models.CharField(max_length=200)
    class Meta:
        db_table = 'permisos'

class compartidos(models.Model):
    id_usuario_receptor = models.ForeignKey(usuarios, on_delete=models.CASCADE, related_name="compartidos_receptor")
    id_usuario_propietario = models.ForeignKey(usuarios, on_delete=models.CASCADE, related_name="compartidos_propietario")
    id_archivos = models.ForeignKey(archivos, on_delete=models.CASCADE)
    id_permiso = models.ForeignKey(permisos, on_delete=models.CASCADE)
    class Meta:
        db_table = 'compartidos'

class duracion_plan(models.Model):
    tiempo_duracion = models.CharField(max_length=100)
    class Meta:
        db_table = 'duracion_plan'

class facturacion_planes(models.Model):
    id_usuario = models.ForeignKey(usuarios, on_delete=models.CASCADE)
    id_plan = models.ForeignKey('planes', on_delete=models.CASCADE)
    id_lugar = models.ForeignKey('lugares', on_delete=models.CASCADE)
    fecha_facturacion = models.DateField()
    class Meta:
        db_table = 'facturacion_planes'

class planes(models.Model):
    id_duracion = models.ForeignKey(duracion_plan, on_delete=models.CASCADE)
    id_oferta = models.ForeignKey('ofertas', on_delete=models.CASCADE)
    nombre_plan = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    espacio_almacenamiento = models.BigIntegerField(blank=True, null=True)
    class Meta:
        db_table = 'planes'

class ofertas(models.Model):
    oferta = models.TextField(blank=True, null=True)
    plan_id_duracion = models.ForeignKey(duracion_plan, on_delete=models.CASCADE)
    class Meta:
        db_table = 'ofertas'

class lugares(models.Model):
    id_tipo_lugar = models.ForeignKey('tipos_lugares', on_delete=models.CASCADE)
    id_lugar_1 = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    nombre_lugar = models.CharField(max_length=500, blank=True, null=True)
    class Meta:
        db_table = 'lugares'

class tipos_lugares(models.Model):
    tipo_lugar = models.CharField(max_length=100)
    class Meta:
        db_table = 'tipos_lugares'

class tipos_modificaciones(models.Model):
    tipo_modificacion = models.CharField(max_length=100)
    class Meta:
        db_table = 'tipos_modificaciones'

class modificaciones(models.Model):
    id_tipo_modificacion = models.ForeignKey(tipos_modificaciones, on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(usuarios, on_delete=models.CASCADE)
    id_archivos = models.ForeignKey(archivos, on_delete=models.CASCADE)
    fecha_modificacion = models.DateField()
    class Meta:
        db_table = 'modificaciones'

class pagos(models.Model):
    id_usuario = models.ForeignKey(usuarios, on_delete=models.CASCADE)
    numuero_tarjeta = models.BigIntegerField(blank=True, null=True)
    fecha_vencimiento = models.DateField(blank=True, null=True)
    firma_autorizada = models.IntegerField(blank=True, null=True)
    class Meta:
        db_table = 'pagos'

class usuario_accesos(models.Model):
    id_acceso = models.ForeignKey(accesos, on_delete=models.CASCADE)
    id_usuario = models.ForeignKey(usuarios, on_delete=models.CASCADE)
    fecha_acceso = models.DateField()
    class Meta:
        db_table = 'usuario_accesos'
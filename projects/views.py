from django.http import HttpResponseNotAllowed, JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import check_password
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from .models import *
import json

# Create your views here.


##Ofertas

class PermisosView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        permiso = list(permisos.objects.values())
        if len(permiso) > 0:
            datos = {'message': "Success", 'permisos': permiso}
        else:
            datos = {'message': "permiso not found..."}
        return JsonResponse(datos)

    def post(self, request):
        #print(request.body)
        jd = json.loads(request.body)
        permisos.objects.create(tipo_permiso=jd['tipo_permiso'])
        datos = {'message': "Success"}
        return JsonResponse(datos)
    
class UsuariosView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, id=0):
        if id > 0:
            usuario_data = list(usuarios.objects.filter(id=id).values())
            if len(usuario_data) > 0:
                usuario = usuario_data[0]
                accesosA = list(accesos.objects.filter(usuario = usuario.get('nombre')).values())
                generoA = genero.objects.filter(id=usuario.get('id_tipo_genero_id')).values_list('tipo_genero', flat=True).first()
                usuario['accesos'] = accesosA
                usuario['id_tipo_genero_id'] = generoA
                datos = {'message': 'Success', 'usuario': usuario}
            else:
                datos = {'message': 'Usuario not found...'}
            return JsonResponse(datos)
        else:
            usuario_data = list(usuarios.objects.values())
            if len(usuario_data) > 0:
                datos = {'message': 'Success', 'usuario': usuario_data}
            else:
                datos = {'message': 'Usuario not found'}
            return JsonResponse(datos)
    
    def post(self, request):
        jd = json.loads(request.body)
        try:
            acceso_usuario = accesos.objects.create(
                usuario = jd['nombre'],
                contrasenia = jd['contrasenia']
            )
            genero_usuario = genero.objects.get(id=jd['id_tipo_genero'])
            usuario = usuarios.objects.create(
                nombre = jd['nombre'],
                apellido = jd['apellido'],
                fecha_nacimiento = jd['fecha_nacimiento'],
                id_acceso = acceso_usuario,
                id_tipo_genero = genero_usuario
            )        
            datos = {'message': 'Success', 'usuario_id': usuario.id}
        except accesos.DoesNotExist:
            datos = {'message': 'Acceso de usuario no encontrado'}
        except genero.DoesNotExist:
            datos = {'message': 'Genero no encontrado'}
        except Exception as e:
            datos = {'message': f'Error: {str(e)}'}
        return JsonResponse(datos)
    
    def put(self, request, id):
        jd = json.loads(request.body)
        usuario_data = list(usuarios.objects.filter(id=id).values())
        if len(usuario_data) > 0:
            try:
                acceso_usuario = accesos.objects.get(id=jd['id_acceso'])
                genero_usuario = genero.objects.get(id=jd['id_tipo_genero'])

                usuario = usuarios.objects.get(id=id)
                usuario.nombre = jd['nombre']
                usuario.apellido = jd['apellido']
                usuario.fecha_nacimiento = jd['fecha_nacimiento']
                usuario.id_acceso = acceso_usuario
                usuario.id_tipo_genero = genero_usuario
                usuario.save()
                datos = {'message': "Success"}
            except accesos.DoesNotExist:
                datos = {'message': 'Acceso de usuario no encontrado'}
            except genero.DoesNotExist:
                datos = {'message': 'Genero no encontrado'}
            except Exception as e:
                datos = {'message': f'Error: {str(e)}'}
        else:
            datos = {'message': 'Usuario not found...'}
        return JsonResponse(datos)
    
    def delete(self, request, id):
        usuario_data = list(usuarios.objects.filter(id=id).values())
        if len(usuario_data) > 0:
            usuarios.objects.filter(id=id).delete()
            datos = {'message': "Success"}
        else:
            datos = {'message': "Usuario not found..."}
        return JsonResponse(datos)

        

class AccesosView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, id=0):
        if id > 0:
            accesos_data = list(accesos.objects.filter(id=id).values())
            if len(accesos_data) > 0:
                acceso = accesos_data[0]
                datos = {'message': "Success", 'acceso': acceso}
            else:
                datos = {'messasge': "Acceso not found..."}
            return JsonResponse(datos)
        else:
            accesos_data = list(accesos.objects.values())
            if len(accesos_data) > 0:
                datos = {'message': "Success", 'acceso': accesos_data}
            else:
                datos = {'messasge': "Acceso not found..."}
            return JsonResponse(datos)
        
    def post(self, request, id=0):
        jd = json.loads(request.body)
        accesos.objects.create(
            usuario = jd['usuario'],
            contrasenia = jd['contrasenia']
        )
        datos = {'message': "Success"}
        return JsonResponse(datos)



class OfertasView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    

    def get(self, request, id=0):
        if id > 0:
            try:
                oferta = ofertas.objects.get(id=id)
                datos = {'message': 'Success', 'oferta': oferta}
            except ofertas.DoesNotExist:
                datos = {'message': 'Oferta no encontrada'}
        else:
            ofertas_list = list(ofertas.objects.values())
            if ofertas_list:
                datos = {'message': 'Success', 'ofertas': ofertas_list}
            else:
                datos = {'message': 'No ofertas found'}
        return JsonResponse(datos)
    

    def post(self, request):
        try:
            jd = json.loads(request.body)
            plan = duracion_plan.objects.get(id=jd['plan_id_duracion'])
            oferta = ofertas.objects.create(
                oferta=jd['oferta'],
                plan_id_duracion=plan
            )
            return JsonResponse({'message': 'Success', 'oferta_id': oferta.id}, status=201)
        except duracion_plan.DoesNotExist:
            return JsonResponse({'message': 'Plan de duración no encontrado'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'message': f'Error: {str(e)}'}, status=500)
        

    def put(self, request, id=0):
        if id > 0:
            try:
                oferta = ofertas.objects.get(id=id)
                jd = json.loads(request.body)
                if 'oferta' in jd:
                    oferta.oferta = jd['oferta']
                if 'plan_id_duracion' in jd:
                    plan = duracion_plan.objects.get(id=jd['plan_id_duracion'])
                    oferta.plan_id_duracion = plan
                oferta.save()
                return JsonResponse({'message': 'Success'}, status=200)
            except ofertas.DoesNotExist:
                return JsonResponse({'message': 'Oferta no encontrada'}, status=404)
            except duracion_plan.DoesNotExist:
                return JsonResponse({'message': 'Plan de duración no encontrado'}, status=400)
            except json.JSONDecodeError:
                return JsonResponse({'message': 'Invalid JSON'}, status=400)
            except Exception as e:
                return JsonResponse({'message': f'Error: {str(e)}'}, status=500)
        else:
            return JsonResponse({'message': 'ID no proporcionado'}, status=400)
        

    def delete(self, request, id=0):
        if id > 0:
            try:
                oferta = ofertas.objects.get(id=id)
                oferta.delete()
                return JsonResponse({'message': 'Oferta eliminada exitosamente'}, status=200)
            except ofertas.DoesNotExist:
                return JsonResponse({'message': 'Oferta no encontrada'}, status=404)
        else:
            return JsonResponse({'message': 'ID no proporcionado'}, status=400)
        

## Pagos

class PagosView(View):

    @method_decorator(csrf_exempt) #post
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # Obtener todos los pagos o un pago específico por ID
    def get(self, request, id=0):
        if id > 0:
            try:
                pago = pagos.objects.get(id=id)
                datos = {
                    'message': 'Success',
                    'pago': {
                        'id': pago.id,
                        'id_usuario': pago.id_usuario.id,
                        'numero_tarjeta': pago.numuero_tarjeta,
                        'fecha_vencimiento': pago.fecha_vencimiento,
                        'firma_autorizada': pago.firma_autorizada
                    }
                }
            except pagos.DoesNotExist:
                datos = {'message': 'Pago no encontrado'}
        else:
            pagos_list = list(pagos.objects.all().values())
            if pagos_list:
                datos = {'message': 'Success', 'pagos': pagos_list}
            else:
                datos = {'message': 'No hay pagos disponibles'}
        return JsonResponse(datos)

    # Crear un nuevo pago
    def post(self, request):
        try:
            jd = json.loads(request.body)
            usuario = usuarios.objects.get(id=jd['id_usuario'])
            pago = pagos.objects.create(
                id_usuario=usuario,
                numuero_tarjeta=jd['numero_tarjeta'],
                fecha_vencimiento=jd['fecha_vencimiento'],
                firma_autorizada=jd['firma_autorizada']
            )
            return JsonResponse({'message': 'Success', 'pago_id': pago.id}, status=201)
        except usuarios.DoesNotExist:
            return JsonResponse({'message': 'Usuario no encontrado'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'message': f'Error: {str(e)}'}, status=500)

    # Actualizar un pago existente
    def put(self, request, id=0):
        if id > 0:
            try:
                jd = json.loads(request.body)
                pago = pagos.objects.get(id=id)

                if 'id_usuario' in jd:
                    try:
                        usuario = usuarios.objects.get(id=jd['id_usuario'])
                        pago.id_usuario = usuario
                    except usuarios.DoesNotExist:
                        return JsonResponse({'message': 'Usuario no encontrado'}, status=400)

                if 'numero_tarjeta' in jd:
                    pago.numuero_tarjeta = jd['numero_tarjeta']
                if 'fecha_vencimiento' in jd:
                    pago.fecha_vencimiento = jd['fecha_vencimiento']
                if 'firma_autorizada' in jd:
                    pago.firma_autorizada = jd['firma_autorizada']

                pago.save()
                return JsonResponse({'message': 'Success'}, status=200)

            except pagos.DoesNotExist:
                return JsonResponse({'message': 'Pago no encontrado'}, status=404)
            except json.JSONDecodeError:
                return JsonResponse({'message': 'Invalid JSON'}, status=400)
            except Exception as e:
                return JsonResponse({'message': f'Error: {str(e)}'}, status=500)
        else:
            return JsonResponse({'message': 'ID no proporcionado'}, status=400)

    # Eliminar un pago existente
    def delete(self, request, id=0):
        if id > 0:
            try:
                pago = pagos.objects.get(id=id)
                pago.delete()
                return JsonResponse({'message': 'Pago eliminado con éxito'}, status=200)
            except pagos.DoesNotExist:
                return JsonResponse({'message': 'Pago no encontrado'}, status=404)
        else:
            return JsonResponse({'message': 'ID no proporcionado'}, status=400)
        
#TABLA ARCHIVOS

class ArchivosView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):
        if id > 0:
            archivo_data = list(archivos.objects.filter(id=id).values('id', 'nombre_archivo', 'fecha_guardado', 'tamanio', 'id_carpeta_id', 'id_tipo_archivo_id', 'id_usuario_id'))
            if len(archivo_data) > 0:
                archivo = archivo_data[0]
                datos = {'message': 'Success', 'archivo': archivo}
            else:
                datos = {'message': 'Archivo no encontrado'}
            return JsonResponse(datos)
        else:
            archivo_data = list(
                archivos.objects
                .select_related('id_usuario')  # Similar a la consulta anterior
                .values(
                    'id',
                    'nombre_archivo',
                    'fecha_guardado',
                    'tamanio',
                    'id_carpeta_id',
                    'id_tipo_archivo_id',
                    'id_usuario_id',
                    'id_usuario__nombre'  # Aquí también se accede al nombre del usuario
                )
            )            
            if len(archivo_data) > 0:
                datos = {'message': 'Success', 'archivos': archivo_data}
            else:
                datos = {'message': 'Archivos no encontrados'}
            return JsonResponse(datos)

    def post(self, request):
        print("Recibí la solicitud POST")
        try:
            jd = json.loads(request.body) 
            print(jd)
            archivos.objects.create(
                nombre_archivo=jd['nombre_archivo'],
                fecha_guardado=jd['fecha_guardado'],
                archivo=0, 
                tamanio=jd['tamanio'],
                id_carpeta_id=jd['id_carpeta'],
                id_tipo_archivo_id=jd['id_tipo_archivo'],
                id_usuario_id=jd['id_usuario']
            )
            datos = {'message': 'Archivo creado exitosamente'}
            print(datos)
            return JsonResponse(datos)
        except Exception as e:
            print("Error en el backend:", e)
            return JsonResponse({"message": "Error en la solicitud"}, status=400)

    def put(self, request, id):
        jd = json.loads(request.body)
        archivo_data = list(archivos.objects.filter(id=id).values())

        if len(archivo_data) > 0:
            archivo = archivos.objects.get(id=id)
            archivo.nombre_archivo = jd['nombre_archivo']
            archivo.fecha_guardado = jd['fecha_guardado']
            archivo.archivo = jd['archivo']  
            archivo.tamanio = jd['tamanio']
            archivo.id_carpeta_id = jd['id_carpeta']
            archivo.id_tipo_archivo_id = jd['id_tipo_archivo']
            archivo.id_usuario_id = jd['id_usuario']
            archivo.save()
            datos = {'message': 'Archivo actualizado exitosamente'}
        else:
            datos = {'message': 'Archivo no encontrado'}

        return JsonResponse(datos)

    def delete(self, request, id):
        archivo_data = list(archivos.objects.filter(id=id).values())

        if len(archivo_data) > 0:
            archivos.objects.filter(id=id).delete()
            datos = {'message': 'Archivo eliminado exitosamente'}
        else:
            datos = {'message': 'Archivo no encontrado'}

        return JsonResponse(datos)
    

#TABLA COMPARTIDOS 

class CompartidosView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):
        if id > 0:
            compartido_data = list(compartidos.objects.filter(id=id).values('id', 'id_archivos_id', 'id_permiso_id', 'id_usuario_propietario_id', 'id_usuario_receptor_id'))
            if len(compartido_data) > 0:
                compartido = compartido_data[0]
                datos = {'message': 'Success', 'compartido': compartido}
            else:
                datos = {'message': 'compartido no encontrado'}
            return JsonResponse(datos)
        else:
            compartido_data = list(compartidos.objects.values('id', 'id_archivos_id', 'id_permiso_id', 'id_usuario_propietario_id', 'id_usuario_receptor_id'))
            if len(compartido_data) > 0:
                datos = {'message': 'Success', 'compartidos': compartido_data}
            else:
                datos = {'message': 'compartidos no encontrados'}
            return JsonResponse(datos)

    def post(self, request):
        jd = json.loads(request.body) 
        compartido = compartidos.objects.create(
            id_archivos_id=jd['id_archivos'],
            id_permiso_id=jd['id_permiso'],
            id_usuario_propietario_id=jd['id_usuario_propietario'],  
            id_usuario_receptor_id=jd['id_usuario_receptor'],
        )
        datos = {'message': 'compartido creado exitosamente'}
        return JsonResponse(datos)

    
#TABLA FACTURACION_PLANES 

class FacturacionPlanesView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):
        if id > 0:
            facturacion_planes_data = list(facturacion_planes.objects.filter(id=id).values('id', 'fecha_facturacion', 'id_lugar_id', 'id_plan_id', 'id_usuario_id'))
            if len(facturacion_planes_data) > 0:
                facturacion_plan = facturacion_planes_data[0]  # Renombrado para evitar conflicto
                datos = {'message': 'Success', 'facturacion_planes': facturacion_plan}
            else:
                datos = {'message': 'facturacion_planes no encontrado'}
            return JsonResponse(datos)
        else:
            facturacion_planes_data = list(facturacion_planes.objects.values('id', 'fecha_facturacion', 'id_lugar_id', 'id_plan_id', 'id_usuario_id'))
            if len(facturacion_planes_data) > 0:
                datos = {'message': 'Success', 'facturacion_planes': facturacion_planes_data}
            else:
                datos = {'message': 'facturacion_planes no encontrados'}
            return JsonResponse(datos)

    def post(self, request):
        jd = json.loads(request.body) 
        # Cambié el nombre de la variable a nuevo_facturacion_plan para evitar conflicto con el modelo
        nuevo_facturacion_plan = facturacion_planes.objects.create(
            fecha_facturacion=jd['fecha_facturacion'],
            id_lugar_id=jd['id_lugar'],
            id_plan_id=jd['id_plan'],  
            id_usuario_id=jd['id_usuario'],
        )
        datos = {'message': 'facturacion_planes creado exitosamente'}
        return JsonResponse(datos)

#TABLA LUGARES

class LugaresView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):
        if id > 0:
            lugares_data = list(lugares.objects.filter(id=id).values('id', 'nombre_lugar', 'id_lugar_1_id', 'id_tipo_lugar_id'))
            if len(lugares_data) > 0:
                lugar = lugares_data[0]
                datos = {'message': 'Success', 'lugares': lugares}
            else:
                datos = {'message': 'lugares no encontrado'}
            return JsonResponse(datos)
        else:
            lugares_data = list(lugares.objects.values('id', 'nombre_lugar', 'id_lugar_1_id', 'id_tipo_lugar_id'))
            if len(lugares_data) > 0:
                datos = {'message': 'Success', 'lugares': lugares_data}
            else:
                datos = {'message': 'lugares no encontrados'}
            return JsonResponse(datos)

    def post(self, request):
        jd = json.loads(request.body) 
        lugar = lugares.objects.create(
            nombre_lugar=jd['nombre_lugar'],
            id_lugar_1_id=jd['id_lugar'],
            id_tipo_lugar_id=jd['id_tipo_lugar'],
        )
        datos = {'message': 'lugares creado exitosamente'}
        return JsonResponse(datos)

    
    def delete(self, request, id):
        lugares_data = list(lugares.objects.filter(id=id).values())

        if len(lugares_data) > 0:
            lugares.objects.filter(id=id).delete()
            datos = {'message': 'lugares eliminado exitosamente'}
        else:
            datos = {'message': 'lugares no encontrado'}

        return JsonResponse(datos)
    
#TABLA MODIFICACIONES

class ModificacionesView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, id=0):
        if id > 0:
            modificaciones_data = list(modificaciones.objects.filter(id=id).values('id', 'id_tipo_modificacion_id', 'id_usuario_id', 'id_archivos_id', 'fecha_modificacion'))
            if len(modificaciones_data) > 0:
                modificacion = modificaciones_data[0]
                datos = {'message': 'Success', 'modificaciones': modificaciones}
            else:
                datos = {'message': 'modificaciones no encontrado'}
            return JsonResponse(datos)
        else:
            modificaciones_data = list(modificaciones.objects.values('id', 'id_tipo_modificacion', 'id_usuario_id', 'id_archivos_id', 'fecha_modificacion'))
            if len(modificaciones_data) > 0:
                datos = {'message': 'Success', 'modificacioness': modificaciones_data}
            else:
                datos = {'message': 'modificacioness no encontrados'}
            return JsonResponse(datos)

    def put(self, request, id):
        jd = json.loads(request.body)
        modificaciones_data = list(modificaciones.objects.filter(id=id).values())

        if len(modificaciones_data) > 0:
            modificacion = modificaciones.objects.get(id=id)
            modificacion.id_tipo_modificacion_id = jd['id_tipo_modificacion']
            modificacion.id_usuario_id = jd['id_usuario']
            modificacion.id_archivos_id = jd['id_archivos']  
            modificacion.fecha_modificacion = jd['fecha_modificacion']
            modificacion.save()
            datos = {'message': 'modificaciones actualizado exitosamente'}
        else:
            datos = {'message': 'modificaciones no encontrado'}

        return JsonResponse(datos) 
        


[sistema_software_fj.py](https://github.com/user-attachments/files/34995980/sistema_software_fj.py)
from abc import ABC, abstractmethod
import datetime
import logging

# Configuración del sistema de logs (requisito de registro de errores y eventos)
logging.basicConfig(
    filename='sistema_errores.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Excepción personalizada (requisito de manejo avanzado de excepciones)
class ErrorOperacionSoftwareFJ(Exception):
    """Excepción base para errores personalizados en el sistema Software FJ."""
    pass

class ClienteInvalidoError(ErrorOperacionSoftwareFJ):
    """Se lanza cuando los datos del cliente no cumplen las validaciones."""
    pass

class ReservaNoDisponibleError(ErrorOperacionSoftwareFJ):
    """Se lanza cuando no es posible procesar una reserva."""
    pass


# 1. Clase Abstracta General (Entidad del sistema)
class EntidadSistema(ABC):
    def __init__(self, identificador: str):
        self._identificador = identificador

    @property
    def identificador(self):
        return self._identificador

    @abstractmethod
    def obtener_detalles(self) -> str:
        pass


# 2. Clase Cliente con encapsulación y validaciones estrictas
class Cliente(EntidadSistema):
    def __init__(self, identificador: str, nombre: str, correo: str, telefono: str):
        super().__init__(identificador)
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not valor or len(valor.strip()) < 3:
            logging.error(f"Intento de registrar cliente con nombre inválido: {valor}")
            raise ClienteInvalidoError("El nombre del cliente debe tener al menos 3 caracteres.")
        self._nombre = valor

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, valor):
        if "@" not in valor or "." not in valor:
            logging.error(f"Intento de registrar cliente con correo inválido: {valor}")
            raise ClienteInvalidoError("El correo electrónico no es válido.")
        self._correo = valor

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        if not valor.isdigit() or len(valor) < 7:
            logging.error(f"Intento de registrar cliente con teléfono inválido: {valor}")
            raise ClienteInvalidoError("El teléfono debe contener solo números y al menos 7 dígitos.")
        self._telefono = valor

    def obtener_detalles(self) -> str:
        return f"Cliente: {self.nombre} | Correo: {self.correo} | Teléfono: {self.telefono}"


# 3. Clase Abstracta Servicio y Servicios Especializados (Herencia y Polimorfismo)
class Servicio(ABC):
    def __init__(self, codigo: str, nombre_servicio: str, costo_base: float):
        self.codigo = codigo
        self.nombre_servicio = nombre_servicio
        self.costo_base = costo_base

    @abstractmethod
    def calcular_costo(self) -> float:
        pass

    @abstractmethod
    def descripcion(self) -> str:
        pass


# Servicio 1: Reserva de Salas
class ReservaSalas(Servicio):
    def __init__(self, codigo: str, costo_base: float, capacidad_personas: int):
        super().__init__(codigo, "Reserva de Salas", costo_base)
        self.capacidad_personas = capacidad_personas

    # Método sobrecargado / con parámetros opcionales para calcular costos con impuestos/descuentos
    def calcular_costo(self, descuento: float = 0.0, impuesto: float = 0.19) -> float:
        try:
            if descuento < 0 or impuesto < 0:
                raise ValueError("Los valores de descuento e impuesto no pueden ser negativos.")
            costo_con_descuento = self.costo_base * (1 - descuento)
            costo_final = costo_con_descuento * (1 + impuesto)
            return round(costo_final, 2)
        except Exception as e:
            logging.error(f"Error calculando costo en ReservaSalas: {e}")
            raise

    def descripcion(self) -> str:
        return f"Servicio de Salas - Capacidad: {self.capacidad_personas} personas. Costo Base: ${self.costo_base}"


# Servicio 2: Alquiler de Equipos
class AlquilerEquipos(Servicio):
    def __init__(self, codigo: str, costo_base: float, tipo_equipo: str):
        super().__init__(codigo, "Alquiler de Equipos", costo_base)
        self.tipo_equipo = tipo_equipo

    def calcular_costo(self, horas_extra: int = 0) -> float:
        try:
            tarifa_hora_extra = 15000.0
            costo_total = self.costo_base + (horas_extra * tarifa_hora_extra)
            return round(costo_total, 2)
        except Exception as e:
            logging.error(f"Error calculando costo en AlquilerEquipos: {e}")
            raise

    def descripcion(self) -> str:
        return f"Alquiler de Equipo: {self.tipo_equipo}. Costo Base: ${self.costo_base}"


# Servicio 3: Asesorías Especializadas
class AsesoriaEspecializada(Servicio):
    def __init__(self, codigo: str, costo_base: float, tecnologia: str):
        super().__init__(codigo, "Asesoría Especializada", costo_base)
        self.tecnologia = tecnologia

    def calcular_costo(self, nivel_complejidad: int = 1) -> float:
        try:
            multiplicador = 1.0 + (nivel_complejidad * 0.1)
            return round(self.costo_base * multiplicador, 2)
        except Exception as e:
            logging.error(f"Error calculando costo en AsesoriaEspecializada: {e}")
            raise

    def descripcion(self) -> str:
        return f"Asesoría en Tecnología: {self.tecnologia}. Costo Base: ${self.costo_base}"


# 4. Clase Reserva que integra cliente, servicio, duración y estado
class Reserva:
    def __init__(self, id_reserva: str, cliente: Cliente, servicio: Servicio, duracion_horas: int):
        self.id_reserva = id_reserva
        self.cliente = cliente
        self.servicio = servicio
        self.duracion_horas = duracion_horas
        self.estado = "Creada"

    def confirmar_reserva(self):
        try:
            if self.duracion_horas <= 0:
                raise ReservaNoDisponibleError("La duración de la reserva debe ser mayor a 0 horas.")
            self.estado = "Confirmada"
            logging.info(f"Reserva {self.id_reserva} confirmada exitosamente.")
            print(f"[ÉXITO] Reserva {self.id_reserva} confirmada para el cliente {self.cliente.nombre}.")
        except ReservaNoDisponibleError as e:
            self.estado = "Fallida"
            logging.error(f"Falla al confirmar reserva {self.id_reserva}: {e}")
            print(f"[ERROR CONTROLADO] No se pudo confirmar la reserva: {e}")
        except Exception as e:
            self.estado = "Error"
            logging.error(f"Error crítico inesperado en reserva {self.id_reserva}: {e}")
            print(f"[ERROR INESPERADO]: {e}")
        finally:
            print(f"-> Estado actual de la reserva {self.id_reserva}: {self.estado}\n")

    def cancelar_reserva(self):
        try:
            if self.estado == "Cancelada":
                raise ReservaNoDisponibleError("La reserva ya se encontraba cancelada.")
            self.estado = "Cancelada"
            logging.info(f"Reserva {self.id_reserva} cancelada correctamente.")
            print(f"[CANCELADA] La reserva {self.id_reserva} ha sido cancelada.")
        except Exception as e:
            logging.error(f"Error al cancelar la reserva {self.id_reserva}: {e}")
            print(f"[ERROR] {e}")


# 5. Simulador de las 10 operaciones (Válidas e Inválidas) con manejo try/except/else/finally
def simular_operaciones_software_fj():
    print("=== INICIANDO SIMULACIÓN DE 10 OPERACIONES - SOFTWARE FJ ===\n")
    
    # Lista interna para almacenar los registros sin base de datos
    operaciones_realizadas = []

    # Operación 1: Registro de Cliente Válido
    print("--- Operación 1: Registro Válido de Cliente ---")
    try:
        c1 = Cliente("C001", "Carlos Pérez", "carlos.perez@email.com", "3001234567")
        operaciones_realizadas.append(c1)
        print(f"Cliente registrado: {c1.obtener_detalles()}")
    except ClienteInvalidoError as e:
        print(f"Error: {e}")
    else:
        print("Validación de cliente 1 exitosa.\n")

    # Operación 2: Registro de Cliente Inválido (Correo incorrecto)
    print("--- Operación 2: Registro Inválido de Cliente (Correo) ---")
    try:
        c_malo = Cliente("C002", "Ana Gómez", "correo-sin-arroba.com", "3109876543")
    except ClienteInvalidoError as e:
        print(f"[Capturado correctamente por try/except] Error de validación: {e}\n")
        logging.info("Excepción controlada de cliente inválido probada exitosamente.")

    # Operación 3: Creación de Servicio de Salas Válido
    print("--- Operación 3: Creación de Servicio (Salas) ---")
    try:
        s1 = ReservaSalas("S001", 100000.0, 15)
        costo = s1.calcular_costo(descuento=0.10, impuesto=0.19)
        print(f"{s1.descripcion()} | Costo con descuento e impuesto: ${costo}")
    except Exception as e:
        print(f"Error: {e}")
    else:
        print("Servicio de salas creado con éxito.\n")

    # Operación 4: Creación de Servicio de Alquiler de Equipos
    print("--- Operación 4: Creación de Servicio (Equipos) ---")
    try:
        s2 = ReservaAlquiler = AlquilerEquipos("S002", 50000.0, "Laptop Core i5")
        costo_eq = ReservaAlquiler.calcular_costo(horas_extra=2)
        print(f"{ReservaAlquiler.descripcion()} | Costo total con 2 horas extra: ${costo_eq}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("Bloque finally ejecutado para la operación de equipos.\n")

    # Operación 5: Creación de Asesoría Especializada
    print("--- Operación 5: Creación de Servicio (Asesoría) ---")
    try:
        s3 = AsesoriaEspecializada("S003", 200000.0, "Python Avanzado")
        costo_asesoria = s3.calcular_costo(nivel_complejidad=2)
        print(f"{s3.descripcion()} | Costo por complejidad: ${costo_asesoria}\n")
    except Exception as e:
        print(f"Error: {e}")

    # Operación 6: Reserva Exitosa
    print("--- Operación 6: Creación y Confirmación de Reserva Válida ---")
    try:
        reserva1 = Reserva("R001", c1, s1, duracion_horas=3)
        reserva1.confirmar_reserva()
        operaciones_realizadas.append(reserva1)
    except Exception as e:
        print(f"Error en reserva: {e}")

    # Operación 7: Reserva Fallida (Duración inválida <= 0)
    print("--- Operación 7: Intento Fallido de Reserva (Duración Cero) ---")
    try:
        reserva_fallida = Reserva("R002", c1, s2, duracion_horas=0)
        reserva_fallida.confirmar_reserva()
    except Exception as e:
        print(f"Error general capturado: {e}\n")

    # Operación 8: Registro de Cliente con Nombre Inválido
    print("--- Operación 8: Registro Inválido de Cliente (Nombre corto) ---")
    try:
        c_corto = Cliente("C003", "Jo", "jo@email.com", "3201112233")
    except ClienteInvalidoError as e:
        print(f"[Capturado con éxito] Validación de nombre: {e}\n")

    # Operación 9: Cancelación de Reserva Existente
    print("--- Operación 9: Cancelación de Reserva ---")
    try:
        reserva1.cancelar_reserva()
    except Exception as e:
        print(f"Error al cancelar: {e}")

    # Operación 10: Intento de cancelar una reserva ya cancelada (Manejo de excepciones)
    print("--- Operación 10: Excepción por cancelar reserva ya inactiva ---")
    try:
        reserva1.cancelar_reserva()
    except Exception as e:
        print(f"Excepción controlada en cancelación doble: {e}")
    finally:
        print("Fin de la simulación de las 10 operaciones de Software FJ.\n")
        print(f"Total de entidades gestionadas en memoria: {len(operaciones_realizadas)}")

if __name__ == "__main__":
    simular_operaciones_software_fj()

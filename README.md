# TP_DAO_GRUPO_22

Repositorio creado para el trabajo práctico de DAO

## Integrantes
- **Cappellari, Julian** 90302
- **Correa, Jeremias** 88714
- **Fragherazzi, Leo** 90162

---

## Enunciado

### Objetivo
Desarrollar un sistema de gestión para un hotel que permita manejar habitaciones, reservas, clientes y facturación.

### Requerimientos

#### Clases:
- **Habitación**:
  - Número
  - Tipo (simple, doble, suite)
  - Estado (disponible/ocupada)
  - Precio por noche

- **Cliente**:
  - ID
  - Nombre
  - Apellido
  - Dirección
  - Teléfono
  - Email

- **Reserva**:
  - ID
  - Cliente
  - Habitación
  - Fecha de entrada
  - Fecha de salida
  - Cantidad de personas

- **Factura**:
  - ID
  - Cliente
  - Reserva
  - Fecha de emisión
  - Total

- **Empleado**:
  - ID
  - Nombre
  - Apellido
  - Cargo (recepcionista, servicio de limpieza, etc.)
  - Sueldo

#### Operaciones:
1. **Registro de Habitaciones**: Permitir el registro de nuevas habitaciones en el sistema.
2. **Registro de Clientes**: Permitir el registro de nuevos clientes.
3. **Registro de Reservas**: Permitir reservar habitaciones y asignarlas a clientes.
4. **Registro de Facturas**: Generar facturas automáticamente al finalizar la estadía del cliente.
5. **Asignación de Empleados a Habitaciones**: Asignar empleados para el servicio de limpieza de las habitaciones.
6. **Consulta de Disponibilidad de Habitaciones**: Consultar la disponibilidad de habitaciones en una fecha específica.

#### Reportes:
- **Listar todas las reservas** realizadas en un periodo de tiempo.
- **Generar un reporte de ingresos** por habitaciones y servicios extras.
- **Reporte de ocupación promedio** por tipo de habitación.

#### Dificultad Extra:
- Incluir validaciones:
  - Verificar que las fechas de reserva no se superpongan para la misma habitación.
  - Verificar que los empleados asignados a habitaciones no tengan más de 5 asignaciones diarias.

- Implementar reportes:
  - Generar un gráfico de barras mostrando la ocupación promedio por tipo de habitación.
  - Generar un gráfico de líneas mostrando los ingresos mensuales.

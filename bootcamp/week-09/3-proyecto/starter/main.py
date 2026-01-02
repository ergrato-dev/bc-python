"""
Proyecto: Sistema de Gestión de Empleados
=========================================
Implementa un sistema de nómina usando herencia y polimorfismo.

Instrucciones:
1. Completa cada clase siguiendo los TODOs
2. Ejecuta para verificar que funciona
3. El resultado debe mostrar un reporte de nómina completo
"""

from datetime import datetime


# ============================================
# MIXIN: TaxableMixin
# ============================================

class TaxableMixin:
    """
    Mixin que añade funcionalidad de cálculo de impuestos.

    Puede usarse con cualquier clase que tenga calculate_pay().
    """

    TAX_RATE = 0.15  # 15% de impuestos

    def calculate_tax(self) -> float:
        """Calcula el impuesto sobre el pago bruto."""
        # TODO: Retornar calculate_pay() * TAX_RATE
        pass

    def net_pay(self) -> float:
        """Calcula el pago neto (después de impuestos)."""
        # TODO: Retornar calculate_pay() - calculate_tax()
        pass


# ============================================
# CLASE BASE: Employee
# ============================================

class Employee:
    """
    Clase base para todos los empleados.

    Attributes:
        name: Nombre completo del empleado
        employee_id: Identificador único
        base_salary: Salario base mensual
    """

    def __init__(
        self,
        name: str,
        employee_id: str,
        base_salary: float
    ) -> None:
        """
        Inicializa un empleado.

        Args:
            name: Nombre del empleado
            employee_id: ID único del empleado
            base_salary: Salario base mensual
        """
        # TODO: Asignar los atributos
        # self.name = ...
        # self.employee_id = ...
        # self.base_salary = ...
        pass

    def calculate_pay(self) -> float:
        """
        Calcula el pago del empleado.

        Returns:
            float: Monto del pago

        Note:
            Este método debe ser sobrescrito por las subclases.
        """
        raise NotImplementedError("Subclasses must implement calculate_pay()")

    def get_info(self) -> str:
        """
        Retorna información básica del empleado.

        Returns:
            str: Información formateada del empleado
        """
        # TODO: Retornar string con formato:
        # "[{employee_id}] {name}"
        pass

    def __str__(self) -> str:
        """Representación string del empleado."""
        return self.get_info()


# ============================================
# CLASE: FullTimeEmployee
# ============================================

class FullTimeEmployee(TaxableMixin, Employee):
    """
    Empleado de tiempo completo con beneficios y bono.

    Attributes:
        benefits: Lista de beneficios del empleado
        bonus_percent: Porcentaje de bono (0.0 a 1.0)
    """

    def __init__(
        self,
        name: str,
        employee_id: str,
        base_salary: float,
        benefits: list[str] | None = None,
        bonus_percent: float = 0.0
    ) -> None:
        """
        Inicializa un empleado de tiempo completo.

        Args:
            name: Nombre del empleado
            employee_id: ID único
            base_salary: Salario base mensual
            benefits: Lista de beneficios (opcional)
            bonus_percent: Porcentaje de bono (default 0.0)
        """
        # TODO: Llamar a super().__init__() con los parámetros correctos
        # TODO: Asignar self.benefits (usar lista vacía si es None)
        # TODO: Asignar self.bonus_percent
        pass

    def calculate_pay(self) -> float:
        """
        Calcula el pago incluyendo el bono.

        Formula: base_salary + (base_salary * bonus_percent)

        Returns:
            float: Pago total con bono
        """
        # TODO: Implementar la fórmula
        pass

    def get_bonus_amount(self) -> float:
        """Retorna el monto del bono."""
        # TODO: Retornar base_salary * bonus_percent
        pass

    def get_info(self) -> str:
        """Retorna información del empleado de tiempo completo."""
        # TODO: Extender get_info() del padre añadiendo el tipo
        # Formato: "[{id}] {name} - Full Time"
        pass


# ============================================
# CLASE: PartTimeEmployee
# ============================================

class PartTimeEmployee(TaxableMixin, Employee):
    """
    Empleado de medio tiempo pagado por horas.

    Attributes:
        hours_worked: Horas trabajadas en el período
        hourly_rate: Tarifa por hora
    """

    def __init__(
        self,
        name: str,
        employee_id: str,
        hourly_rate: float,
        hours_worked: float = 0.0
    ) -> None:
        """
        Inicializa un empleado de medio tiempo.

        Args:
            name: Nombre del empleado
            employee_id: ID único
            hourly_rate: Tarifa por hora
            hours_worked: Horas trabajadas (default 0.0)
        """
        # TODO: Llamar a super().__init__() con base_salary=0
        # TODO: Asignar hourly_rate y hours_worked
        pass

    def calculate_pay(self) -> float:
        """
        Calcula el pago basado en horas trabajadas.

        Formula: hours_worked * hourly_rate

        Returns:
            float: Pago total por horas
        """
        # TODO: Implementar la fórmula
        pass

    def log_hours(self, hours: float) -> None:
        """
        Registra horas trabajadas adicionales.

        Args:
            hours: Horas a añadir
        """
        # TODO: Añadir hours a hours_worked
        pass

    def get_info(self) -> str:
        """Retorna información del empleado de medio tiempo."""
        # TODO: Formato: "[{id}] {name} - Part Time"
        pass


# ============================================
# CLASE: Contractor
# ============================================

class Contractor(Employee):
    """
    Contratista externo por proyecto.

    Note:
        Los contratistas NO usan TaxableMixin porque
        manejan sus propios impuestos.

    Attributes:
        hourly_rate: Tarifa por hora
        hours_billed: Horas facturadas
        project_name: Nombre del proyecto actual
    """

    def __init__(
        self,
        name: str,
        employee_id: str,
        hourly_rate: float,
        project_name: str,
        hours_billed: float = 0.0
    ) -> None:
        """
        Inicializa un contratista.

        Args:
            name: Nombre del contratista
            employee_id: ID único
            hourly_rate: Tarifa por hora
            project_name: Nombre del proyecto
            hours_billed: Horas facturadas (default 0.0)
        """
        # TODO: Llamar a super().__init__() con base_salary=0
        # TODO: Asignar hourly_rate, project_name, hours_billed
        pass

    def calculate_pay(self) -> float:
        """
        Calcula el pago basado en horas facturadas.

        Formula: hours_billed * hourly_rate

        Returns:
            float: Pago total facturado
        """
        # TODO: Implementar la fórmula
        pass

    def bill_hours(self, hours: float) -> None:
        """
        Factura horas adicionales al proyecto.

        Args:
            hours: Horas a facturar
        """
        # TODO: Añadir hours a hours_billed
        pass

    def get_info(self) -> str:
        """Retorna información del contratista."""
        # TODO: Formato: "[{id}] {name} - Contractor ({project_name})"
        pass


# ============================================
# CLASE: Manager
# ============================================

class Manager(FullTimeEmployee):
    """
    Gerente que hereda de FullTimeEmployee.

    Recibe un bono adicional basado en el tamaño de su equipo.

    Attributes:
        department: Departamento que dirige
        team_size: Número de empleados en el equipo
    """

    TEAM_BONUS_PER_MEMBER = 100  # $100 por cada miembro del equipo

    def __init__(
        self,
        name: str,
        employee_id: str,
        base_salary: float,
        department: str,
        team_size: int = 0,
        benefits: list[str] | None = None,
        bonus_percent: float = 0.0
    ) -> None:
        """
        Inicializa un gerente.

        Args:
            name: Nombre del gerente
            employee_id: ID único
            base_salary: Salario base mensual
            department: Departamento que dirige
            team_size: Tamaño del equipo (default 0)
            benefits: Lista de beneficios
            bonus_percent: Porcentaje de bono
        """
        # TODO: Llamar a super().__init__() con los parámetros de FullTimeEmployee
        # TODO: Asignar department y team_size
        pass

    def calculate_pay(self) -> float:
        """
        Calcula el pago incluyendo bono de equipo.

        Formula: super().calculate_pay() + (team_size * TEAM_BONUS_PER_MEMBER)

        Returns:
            float: Pago total con bono de equipo
        """
        # TODO: Implementar usando super().calculate_pay()
        pass

    def get_team_bonus(self) -> float:
        """Retorna el bono por tamaño de equipo."""
        # TODO: Retornar team_size * TEAM_BONUS_PER_MEMBER
        pass

    def add_team_member(self) -> None:
        """Incrementa el tamaño del equipo en 1."""
        # TODO: Incrementar team_size
        pass

    def remove_team_member(self) -> None:
        """Decrementa el tamaño del equipo en 1 (mínimo 0)."""
        # TODO: Decrementar team_size si es > 0
        pass

    def get_info(self) -> str:
        """Retorna información del gerente."""
        # TODO: Formato: "[{id}] {name} - Manager ({department})"
        pass


# ============================================
# CLASE: Payroll
# ============================================

class Payroll:
    """
    Sistema de nómina que gestiona todos los empleados.

    Attributes:
        employees: Diccionario de empleados por ID
        pay_period: Período de pago actual
    """

    def __init__(self, pay_period: str | None = None) -> None:
        """
        Inicializa el sistema de nómina.

        Args:
            pay_period: Período de pago (default: mes actual)
        """
        self.employees: dict[str, Employee] = {}
        self.pay_period = pay_period or datetime.now().strftime("%B %Y")

    def add_employee(self, employee: Employee) -> None:
        """
        Añade un empleado al sistema.

        Args:
            employee: Empleado a añadir
        """
        # TODO: Añadir employee al diccionario usando employee_id como key
        pass

    def remove_employee(self, employee_id: str) -> bool:
        """
        Elimina un empleado del sistema.

        Args:
            employee_id: ID del empleado a eliminar

        Returns:
            bool: True si se eliminó, False si no existía
        """
        # TODO: Eliminar del diccionario si existe, retornar True/False
        pass

    def get_employee(self, employee_id: str) -> Employee | None:
        """
        Obtiene un empleado por ID.

        Args:
            employee_id: ID del empleado

        Returns:
            Employee o None si no existe
        """
        # TODO: Retornar el empleado o None
        pass

    def get_total_payroll(self) -> float:
        """
        Calcula el total de la nómina (pagos brutos).

        Returns:
            float: Suma de todos los pagos
        """
        # TODO: Sumar calculate_pay() de todos los empleados
        pass

    def get_total_tax(self) -> float:
        """
        Calcula el total de impuestos retenidos.

        Returns:
            float: Suma de impuestos (solo empleados con TaxableMixin)
        """
        # TODO: Sumar calculate_tax() de empleados que tengan ese método
        # Hint: usa hasattr(employee, 'calculate_tax')
        pass

    def generate_report(self) -> str:
        """
        Genera un reporte completo de nómina.

        Returns:
            str: Reporte formateado
        """
        lines = []
        lines.append("=" * 50)
        lines.append(f"       PAYROLL REPORT - {self.pay_period}")
        lines.append("=" * 50)
        lines.append("")

        # TODO: Agrupar empleados por tipo y generar secciones
        # - FULL-TIME EMPLOYEES (FullTimeEmployee pero no Manager)
        # - MANAGERS
        # - PART-TIME EMPLOYEES
        # - CONTRACTORS

        # Para cada empleado mostrar:
        # - get_info()
        # - Detalles específicos del tipo
        # - Gross Pay, Tax (si aplica), Net Pay (si aplica)

        # Al final, mostrar SUMMARY con totales

        # Por ahora, retorna un placeholder
        lines.append("TODO: Implementar generación de reporte")
        lines.append("")
        lines.append("=" * 50)

        return "\n".join(lines)


# ============================================
# FUNCIÓN PRINCIPAL
# ============================================

def main() -> None:
    """Función principal que demuestra el sistema."""

    print("Sistema de Gestión de Empleados")
    print("=" * 40)
    print()

    # TODO: Crear instancias de cada tipo de empleado

    # Empleado de tiempo completo
    # ana = FullTimeEmployee(
    #     name="Ana García",
    #     employee_id="FT001",
    #     base_salary=5000,
    #     benefits=["Health Insurance", "401k", "Dental"],
    #     bonus_percent=0.10
    # )

    # Gerente
    # carlos = Manager(
    #     name="Carlos López",
    #     employee_id="MGR01",
    #     base_salary=7000,
    #     department="Engineering",
    #     team_size=5,
    #     benefits=["Health Insurance", "401k", "Dental", "Stock Options"],
    #     bonus_percent=0.15
    # )

    # Empleado de medio tiempo
    # maria = PartTimeEmployee(
    #     name="María Rodríguez",
    #     employee_id="PT001",
    #     hourly_rate=25,
    #     hours_worked=80
    # )

    # Contratista
    # david = Contractor(
    #     name="David Kim",
    #     employee_id="CON01",
    #     hourly_rate=75,
    #     project_name="Cloud Migration",
    #     hours_billed=120
    # )

    # TODO: Crear sistema de nómina y añadir empleados
    # payroll = Payroll()
    # payroll.add_employee(ana)
    # payroll.add_employee(carlos)
    # payroll.add_employee(maria)
    # payroll.add_employee(david)

    # TODO: Generar y mostrar reporte
    # print(payroll.generate_report())

    print("TODO: Implementar las clases y descomentar el código")


if __name__ == "__main__":
    main()

# 🏢 Proyecto: Sistema de Gestión de Empleados

## 📋 Descripción

Desarrollarás un **Sistema de Gestión de Empleados** que utiliza herencia y polimorfismo para modelar diferentes tipos de empleados en una empresa, cada uno con su propia forma de calcular salario y beneficios.

---

## 🎯 Objetivos de Aprendizaje

- Aplicar herencia para crear jerarquías de clases
- Usar `super()` para extender funcionalidad
- Implementar polimorfismo para cálculos de salario
- Crear Mixins para funcionalidad compartida
- Diseñar código extensible y mantenible

---

## 📊 Diagrama de Clases

```
                    ┌─────────────────┐
                    │    Employee     │ (Base)
                    │─────────────────│
                    │ - name          │
                    │ - employee_id   │
                    │ - base_salary   │
                    │─────────────────│
                    │ + calculate_pay()│
                    │ + get_info()    │
                    └────────┬────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
         ▼                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ FullTimeEmployee│ │PartTimeEmployee │ │   Contractor    │
│─────────────────│ │─────────────────│ │─────────────────│
│ - benefits      │ │ - hours_worked  │ │ - hourly_rate   │
│ - bonus_percent │ │ - hourly_rate   │ │ - hours_billed  │
│─────────────────│ │─────────────────│ │ - project_name  │
│ + calculate_pay()│ │ + calculate_pay()│ │ + calculate_pay()│
└─────────────────┘ └─────────────────┘ └─────────────────┘
         │
         ▼
┌─────────────────┐
│    Manager      │ (Hereda de FullTimeEmployee)
│─────────────────│
│ - team_size     │
│ - department    │
│─────────────────│
│ + calculate_pay()│ (+ bono por equipo)
│ + add_team_member()│
└─────────────────┘
```

---

## 🔧 Requisitos Funcionales

### 1. Clase Base `Employee`

| Atributo | Tipo | Descripción |
|----------|------|-------------|
| `name` | `str` | Nombre del empleado |
| `employee_id` | `str` | ID único |
| `base_salary` | `float` | Salario base mensual |

| Método | Retorno | Descripción |
|--------|---------|-------------|
| `calculate_pay()` | `float` | Calcula el pago (override en subclases) |
| `get_info()` | `str` | Información del empleado |

---

### 2. Clase `FullTimeEmployee`

Empleado de tiempo completo con beneficios y bonos.

| Atributo Adicional | Tipo | Descripción |
|--------------------|------|-------------|
| `benefits` | `list[str]` | Lista de beneficios |
| `bonus_percent` | `float` | Porcentaje de bono (0.0 - 1.0) |

**Cálculo de pago:**
```
pago = base_salary + (base_salary * bonus_percent)
```

---

### 3. Clase `PartTimeEmployee`

Empleado de medio tiempo pagado por horas.

| Atributo Adicional | Tipo | Descripción |
|--------------------|------|-------------|
| `hours_worked` | `float` | Horas trabajadas en el período |
| `hourly_rate` | `float` | Tarifa por hora |

**Cálculo de pago:**
```
pago = hours_worked * hourly_rate
```

---

### 4. Clase `Contractor`

Contratista externo por proyecto.

| Atributo Adicional | Tipo | Descripción |
|--------------------|------|-------------|
| `hourly_rate` | `float` | Tarifa por hora |
| `hours_billed` | `float` | Horas facturadas |
| `project_name` | `str` | Nombre del proyecto |

**Cálculo de pago:**
```
pago = hours_billed * hourly_rate
```

---

### 5. Clase `Manager`

Gerente que hereda de `FullTimeEmployee` con bono adicional por equipo.

| Atributo Adicional | Tipo | Descripción |
|--------------------|------|-------------|
| `department` | `str` | Departamento que dirige |
| `team_size` | `int` | Número de empleados en el equipo |

**Cálculo de pago:**
```
pago_base = super().calculate_pay()  # Pago de FullTimeEmployee
bono_equipo = team_size * 100  # $100 por cada miembro del equipo
pago_total = pago_base + bono_equipo
```

---

### 6. Mixin `TaxableMixin`

Añade funcionalidad de cálculo de impuestos.

```python
class TaxableMixin:
    TAX_RATE = 0.15  # 15% de impuestos

    def calculate_tax(self) -> float:
        """Calcula el impuesto sobre el pago."""
        return self.calculate_pay() * self.TAX_RATE

    def net_pay(self) -> float:
        """Calcula el pago neto después de impuestos."""
        return self.calculate_pay() - self.calculate_tax()
```

---

### 7. Clase `Payroll`

Sistema de nómina que procesa todos los empleados.

| Método | Descripción |
|--------|-------------|
| `add_employee(employee)` | Añade empleado al sistema |
| `remove_employee(employee_id)` | Elimina empleado por ID |
| `process_payroll()` | Procesa nómina de todos |
| `get_total_payroll()` | Suma total de pagos |
| `generate_report()` | Genera reporte detallado |

---

## 📁 Estructura del Proyecto

```
3-proyecto/
├── README.md
├── starter/
│   └── main.py          # Código inicial con TODOs
└── solution/
    └── main.py          # Solución completa (oculta)
```

---

## 🚀 Instrucciones

1. Abre `starter/main.py`
2. Implementa cada clase siguiendo los TODOs
3. Ejecuta el código para verificar
4. El programa debe mostrar un reporte de nómina completo

---

## ✅ Resultado Esperado

```
========================================
       PAYROLL REPORT - January 2026
========================================

FULL-TIME EMPLOYEES:
--------------------
[FT001] Ana García - Software Engineer
  Base Salary: $5,000.00
  Bonus (10%): $500.00
  Gross Pay:   $5,500.00
  Tax (15%):   $825.00
  Net Pay:     $4,675.00
  Benefits: Health Insurance, 401k, Dental

[MGR01] Carlos López - Engineering Manager
  Base Salary: $7,000.00
  Bonus (15%): $1,050.00
  Team Bonus:  $500.00 (5 members)
  Gross Pay:   $8,550.00
  Tax (15%):   $1,282.50
  Net Pay:     $7,267.50
  Department: Engineering

PART-TIME EMPLOYEES:
--------------------
[PT001] María Rodríguez - Support Specialist
  Hours Worked: 80.0
  Hourly Rate:  $25.00
  Gross Pay:    $2,000.00
  Tax (15%):    $300.00
  Net Pay:      $1,700.00

CONTRACTORS:
------------
[CON01] David Kim - DevOps Consultant
  Project: Cloud Migration
  Hours Billed: 120.0
  Hourly Rate:  $75.00
  Gross Pay:    $9,000.00
  (No tax withholding for contractors)

========================================
SUMMARY
========================================
Total Employees:     4
Total Gross Payroll: $25,050.00
Total Tax Withheld:  $2,407.50
Total Net Payroll:   $22,642.50
========================================
```

---

## 🎯 Criterios de Evaluación

| Criterio | Puntos |
|----------|--------|
| Herencia correcta entre clases | 20 |
| Uso apropiado de `super()` | 15 |
| Polimorfismo en `calculate_pay()` | 20 |
| Implementación del Mixin | 15 |
| Clase Payroll funcional | 15 |
| Código limpio y documentado | 10 |
| Manejo de edge cases | 5 |
| **Total** | **100** |

---

## 💡 Consejos

1. **Empieza por la clase base** `Employee` - es la fundación
2. **Prueba cada clase** individualmente antes de integrar
3. **Usa type hints** en todos los métodos
4. **El Mixin** debe funcionar con cualquier clase que tenga `calculate_pay()`
5. **Manager hereda de FullTimeEmployee**, no directamente de Employee

---

## 🔗 Recursos

- [Herencia en Python](../1-teoria/01-herencia-basica.md)
- [super() y Override](../1-teoria/02-super-y-override.md)
- [Polimorfismo](../1-teoria/03-polimorfismo.md)
- [Herencia Múltiple y Mixins](../1-teoria/04-herencia-multiple.md)

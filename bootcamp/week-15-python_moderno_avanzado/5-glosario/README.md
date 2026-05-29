# 📖 Glosario — Semana 15: Python Moderno Avanzado

## A

**`ABC` (Abstract Base Class)**
Clase base abstracta del módulo `abc`. Define contratos mediante herencia explícita. Las clases que la implementan *deben* heredar de ella. Contrasta con `Protocol`.

**Annotation**
La anotación de tipo de una variable, parámetro o valor de retorno. Ej: `name: str`, `def f(x: int) -> bool:`.

## C

**Capture pattern**
En `match/case`, un patrón que asigna el valor a una variable nueva. Ej: `case x:` — siempre hace match y asigna a `x`. Diferente de un literal como `case "start":`.

**Class pattern**
En `match/case`, un patrón que verifica el tipo de un objeto y desempaqueta sus atributos. Ej: `case VideoAsset(name=n, codec="h264"):`.

## D

**Dataclass**
Clase decorada con `@dataclass` que genera automáticamente `__init__`, `__repr__` y `__eq__` a partir de las anotaciones de tipo.

**Duck typing**
Filosofía de Python: un objeto es válido si tiene los métodos esperados, sin importar su tipo declarado. `Protocol` formaliza el duck typing con verificación estática.

## F

**`field()`**
Función de `dataclasses` para controlar el comportamiento de un campo: `default_factory`, `repr`, `compare`, `init`, `hash`, `metadata`.

**`frozen=True`**
Parámetro de `@dataclass` que hace la instancia inmutable. Lanza `FrozenInstanceError` al intentar modificar atributos. También habilita `__hash__`.

## G

**Generic / Genérico**
Clase o función que trabaja con un tipo especificado en el punto de uso. Ej: `list[str]`. Se define con `TypeVar` o la sintaxis `[T]` de Python 3.12+.

**Guard**
En `match/case`, una condición adicional después del patrón: `case x if x > 0:`. Solo hace match si la condición es `True`.

## I

**`InitVar`**
Tipo especial de `dataclasses` para parámetros que se reciben en `__init__` pero no se almacenan como atributos. Disponibles solo en `__post_init__`.

## K

**`KW_ONLY`**
Sentinel de `dataclasses`. Todos los campos declarados después de `_: KW_ONLY` son keyword-only en el constructor.

## M

**Mapping pattern**
En `match/case`, un patrón que hace match con diccionarios por sus claves. Son parciales: el dict puede tener más claves que las del patrón.

**mypy**
Type checker estático para Python. Analiza anotaciones de tipo sin ejecutar el código.

## N

**Narrowing**
Proceso por el que el type checker reduce el tipo posible de una variable después de una condición. Ej: después de `if isinstance(x, str):`, `x` es `str` dentro del bloque.

**Nominal typing**
Sistema de tipos donde la compatibilidad se basa en el linaje (herencia). `ABC` usa subtipado nominal.

## P

**`ParamSpec`**
`TypeVar` para la lista de parámetros de una función. Permite decoradores que preservan la firma completa de la función decorada.

**`Protocol`**
Clase del módulo `typing` que define un contrato estructural. Las clases satisfacen el Protocol si tienen los métodos/atributos requeridos, sin heredarlo.

**`__post_init__`**
Método especial de dataclasses que se ejecuta al final de `__init__`. Usado para validación y cómputo de atributos derivados.

## R

**`@runtime_checkable`**
Decorador de `Protocol` que habilita `isinstance()` en runtime. Solo verifica existencia de atributos, no sus tipos.

## S

**`Self`**
Tipo especial (Python 3.11+) que representa "la clase actual". Permite que factories y builders indiquen que retornan la misma clase, incluyendo subclases.

**`__slots__`**
Reemplaza el `__dict__` dinámico de las instancias por un array fijo. Reduce el uso de memoria ~30%. En dataclasses se activa con `slots=True`.

**Structural typing**
Sistema de tipos donde la compatibilidad se basa en la estructura (métodos/atributos), no en el linaje. `Protocol` implementa subtipado estructural.

## T

**`type` keyword**
Keyword de Python 3.12+ para definir aliases de tipo. `type ProjectId = int`. Preferido sobre `TypeAlias` en código nuevo.

**`TypeAlias`**
Forma de Python 3.10/3.11 para declarar un alias de tipo: `ProjectId: TypeAlias = int`.

**Type checker**
Herramienta que analiza anotaciones de tipo sin ejecutar el código. Ejemplos: mypy, pyright, pyrefly.

**`TypeGuard`**
Tipo de retorno que le dice al type checker que si la función retorna `True`, el argumento es del tipo especificado. Habilita narrowing con validaciones complejas.

**`TypeIs`**
Versión mejorada de `TypeGuard` (Python 3.13+) que también hace narrowing en el bloque `else`.

**`TypeVar`**
Variable de tipo para funciones y clases genéricas. En Python 3.12+ se usa la sintaxis `[T]` directamente.

## W

**Wildcard pattern**
En `match/case`, el patrón `_` que hace match con cualquier valor sin asignarlo. Siempre al final como catch-all.

#!/usr/bin/env python3
"""
Ejercicio 1: Sistema de Plugins con ABC
========================================
Aprende a crear clases abstractas y un sistema de plugins extensible.

Instrucciones:
1. Lee cada sección y descomenta el código correspondiente
2. Ejecuta el archivo después de cada paso para verificar
3. Observa cómo las clases abstractas definen contratos
"""

from abc import ABC, abstractmethod


# ============================================
# PASO 1: Clase Abstracta Base
# ============================================
print("=== Sistema de Plugins con ABC ===\n")

# Las clases abstractas definen un CONTRATO que las subclases
# deben cumplir. No pueden ser instanciadas directamente.

# Descomenta la siguiente clase abstracta:

# class TextPlugin(ABC):
#     """
#     Plugin abstracto para procesar texto.
#
#     Todos los plugins deben implementar:
#     - name: Propiedad que retorna el nombre único del plugin
#     - process: Método que transforma el texto
#     """
#
#     @property
#     @abstractmethod
#     def name(self) -> str:
#         """Nombre único del plugin."""
#         ...
#
#     @abstractmethod
#     def process(self, text: str) -> str:
#         """Procesa el texto y retorna el resultado."""
#         ...
#
#     # Método concreto - compartido por todas las subclases
#     def describe(self) -> str:
#         """Descripción del plugin."""
#         return f"Plugin: {self.name}"


# Verificar que no se puede instanciar
print("--- Paso 1: Verificar que TextPlugin es abstracta ---")

# Descomenta para probar:
# try:
#     plugin = TextPlugin()  # Esto debe fallar
# except TypeError as e:
#     print(f"✓ No se puede instanciar TextPlugin directamente")
#     # print(f"  Error: {e}")


# ============================================
# PASO 2: Implementar Plugins Concretos
# ============================================
print("\n--- Paso 2: Plugins concretos ---")

# Cada plugin hereda de TextPlugin e implementa los métodos abstractos.
# Descomenta las siguientes clases:

# class UppercasePlugin(TextPlugin):
#     """Plugin que convierte texto a mayúsculas."""
#
#     @property
#     def name(self) -> str:
#         return "uppercase"
#
#     def process(self, text: str) -> str:
#         return text.upper()


# class ReversePlugin(TextPlugin):
#     """Plugin que invierte el texto."""
#
#     @property
#     def name(self) -> str:
#         return "reverse"
#
#     def process(self, text: str) -> str:
#         return text[::-1]


# class CensorPlugin(TextPlugin):
#     """Plugin que censura vocales intermedias."""
#
#     def __init__(self, censor_char: str = "*"):
#         self.censor_char = censor_char
#
#     @property
#     def name(self) -> str:
#         return "censor"
#
#     def process(self, text: str) -> str:
#         result = []
#         for word in text.split():
#             if len(word) > 2:
#                 # Mantener primera y última letra, censurar el resto
#                 censored = word[0] + self.censor_char * (len(word) - 2) + word[-1]
#                 result.append(censored)
#             else:
#                 result.append(word)
#         return " ".join(result)


# Probar los plugins
# Descomenta para probar:

# text = "Hello World"
# print(f"Original: {text}")
#
# upper = UppercasePlugin()
# print(f"{upper.name}: {upper.process(text)}")
#
# reverse = ReversePlugin()
# print(f"{reverse.name}: {reverse.process(text)}")
#
# censor = CensorPlugin()
# print(f"{censor.name}: {censor.process(text)}")


# ============================================
# PASO 3: Crear el PluginManager
# ============================================
print("\n--- Paso 3: PluginManager ---")

# El PluginManager registra y ejecuta plugins de forma centralizada.
# Descomenta la siguiente clase:

# class PluginManager:
#     """Gestor de plugins de texto."""
#
#     def __init__(self):
#         self._plugins: dict[str, TextPlugin] = {}
#
#     def register(self, plugin: TextPlugin) -> None:
#         """Registra un plugin."""
#         if plugin.name in self._plugins:
#             raise ValueError(f"Plugin '{plugin.name}' already registered")
#         self._plugins[plugin.name] = plugin
#         print(f"  Registrado: {plugin.describe()}")
#
#     def unregister(self, name: str) -> None:
#         """Elimina un plugin del registro."""
#         if name in self._plugins:
#             del self._plugins[name]
#
#     def get_plugin(self, name: str) -> TextPlugin:
#         """Obtiene un plugin por nombre."""
#         if name not in self._plugins:
#             raise KeyError(f"Plugin '{name}' not found")
#         return self._plugins[name]
#
#     def process(self, plugin_name: str, text: str) -> str:
#         """Procesa texto con un plugin específico."""
#         plugin = self.get_plugin(plugin_name)
#         return plugin.process(text)
#
#     def process_pipeline(self, plugin_names: list[str], text: str) -> str:
#         """Procesa texto a través de múltiples plugins en secuencia."""
#         result = text
#         for name in plugin_names:
#             result = self.process(name, result)
#         return result
#
#     @property
#     def available_plugins(self) -> list[str]:
#         """Lista de plugins disponibles."""
#         return list(self._plugins.keys())


# Usar el PluginManager
# Descomenta para probar:

# manager = PluginManager()
#
# # Registrar plugins
# manager.register(UppercasePlugin())
# manager.register(ReversePlugin())
# manager.register(CensorPlugin())
#
# print(f"\nPlugins registrados: {manager.available_plugins}")
#
# # Procesar texto
# text = "Python is awesome!"
# print(f"Procesando '{text}' con uppercase: {manager.process('uppercase', text)}")
# print(f"Procesando '{text}' con reverse: {manager.process('reverse', text)}")


# ============================================
# PASO 4: Pipeline de Plugins
# ============================================
print("\n--- Paso 4: Pipeline de plugins ---")

# Podemos encadenar múltiples plugins para transformaciones complejas.
# Descomenta para probar:

# text = "secret password here"
# pipeline = ["censor", "uppercase"]
#
# result = manager.process_pipeline(pipeline, text)
# print(f"Input: {text}")
# print(f"Pipeline {pipeline}: {result}")


# ============================================
# PASO 5: Agregar Nuevo Plugin Dinámicamente
# ============================================
print("\n--- Paso 5: Agregar nuevo plugin dinámicamente ---")

# Una ventaja del sistema es que podemos añadir plugins sin modificar código existente.
# Descomenta el siguiente plugin:

# class SpacerPlugin(TextPlugin):
#     """Plugin que añade espacios entre caracteres."""
#
#     def __init__(self, separator: str = " "):
#         self.separator = separator
#
#     @property
#     def name(self) -> str:
#         return "spaces"
#
#     def process(self, text: str) -> str:
#         return self.separator.join(text)


# Registrar y usar el nuevo plugin
# Descomenta para probar:

# spacer = SpacerPlugin()
# manager.register(spacer)
# print(f"Nuevo plugin '{spacer.name}' registrado")
# print(f"{spacer.name}('Hello'): {manager.process('spaces', 'Hello')}")


# ============================================
# PASO 6: Verificación de Tipos (Bonus)
# ============================================
print("\n--- Paso 6: Verificación de tipos ---")

# Podemos verificar que un objeto es un TextPlugin válido.
# Descomenta para probar:

# def is_valid_plugin(obj: object) -> bool:
#     """Verifica si un objeto es un plugin válido."""
#     return isinstance(obj, TextPlugin)
#
# print(f"UppercasePlugin es TextPlugin: {is_valid_plugin(UppercasePlugin())}")
# print(f"str es TextPlugin: {is_valid_plugin('not a plugin')}")
#
# # Ver métodos abstractos de TextPlugin
# print(f"\nMétodos abstractos de TextPlugin: {TextPlugin.__abstractmethods__}")


# ============================================
# RESUMEN
# ============================================
print("\n" + "=" * 50)
print("✅ Ejercicio completado!")
print("=" * 50)
print("""
Conceptos aprendidos:
1. ABC y @abstractmethod definen contratos obligatorios
2. Las clases abstractas no pueden instanciarse
3. Las subclases DEBEN implementar todos los métodos abstractos
4. Métodos concretos en ABC son compartidos por subclases
5. PluginManager permite extensibilidad sin modificar código
""")

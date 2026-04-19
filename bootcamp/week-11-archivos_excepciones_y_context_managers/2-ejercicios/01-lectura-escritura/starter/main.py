"""
Ejercicio 01: Lectura y Escritura de Archivos
=============================================

Aprende a manejar archivos en Python de forma correcta y eficiente.

Instrucciones:
1. Lee cada sección y descomenta el código correspondiente
2. Ejecuta el script después de cada paso
3. Observa los resultados y experimenta

Ejecutar:
    python main.py
"""

from pathlib import Path
import csv
import json
import tempfile


def main() -> None:
    """Función principal del ejercicio."""

    print("=" * 60)
    print("EJERCICIO: Lectura y Escritura de Archivos")
    print("=" * 60)

    # Crear directorio temporal para el ejercicio
    with tempfile.TemporaryDirectory() as temp_dir:
        work_dir = Path(temp_dir)

        # ============================================
        # PASO 1: Lectura Básica de Archivos
        # ============================================
        print("\n--- Paso 1: Lectura Básica ---")

        # Primero creamos un archivo de prueba
        test_file = work_dir / "ejemplo.txt"
        test_file.write_text(
            "Hola, este es un archivo de prueba.\n"
            "Segunda línea del archivo.\n"
            "Tercera línea con ñ y acentos: áéíóú\n",
            encoding="utf-8"
        )

        # Descomenta las siguientes líneas:
        # content = test_file.read_text(encoding="utf-8")
        # print(f"Contenido del archivo:\n{content}")
        # print(f"Caracteres totales: {len(content)}")

        # ============================================
        # PASO 2: Escritura de Archivos
        # ============================================
        print("\n--- Paso 2: Escritura de Archivos ---")

        # Método 1: write_text (simple)
        # Descomenta las siguientes líneas:
        # output_file = work_dir / "salida.txt"
        # output_file.write_text("Contenido escrito con write_text\n", encoding="utf-8")
        # print(f"Archivo creado: {output_file.name}")

        # Método 2: with open() (más control)
        # Descomenta las siguientes líneas:
        # with open(work_dir / "salida2.txt", "w", encoding="utf-8") as f:
        #     f.write("Primera línea\n")
        #     f.write("Segunda línea\n")
        #     f.write("Tercera línea\n")
        # print("Archivo salida2.txt creado con open()")

        # ============================================
        # PASO 3: Lectura Línea por Línea
        # ============================================
        print("\n--- Paso 3: Lectura Línea por Línea ---")

        # Crear archivo con varias líneas
        multi_line = work_dir / "lineas.txt"
        multi_line.write_text(
            "Línea 1: Python es genial\n"
            "Línea 2: Los archivos son importantes\n"
            "Línea 3: El encoding UTF-8 es estándar\n"
            "Línea 4: Siempre usar context managers\n"
            "Línea 5: pathlib es moderno\n",
            encoding="utf-8"
        )

        # Descomenta las siguientes líneas:
        # print("Leyendo línea por línea:")
        # with open(multi_line, "r", encoding="utf-8") as f:
        #     for numero, linea in enumerate(f, start=1):
        #         print(f"  {numero}: {linea.strip()}")

        # ============================================
        # PASO 4: Modos de Apertura
        # ============================================
        print("\n--- Paso 4: Modos de Apertura ---")

        # Modo 'w' - Sobrescribe el archivo
        # Descomenta las siguientes líneas:
        # test_modes = work_dir / "modos.txt"
        # with open(test_modes, "w", encoding="utf-8") as f:
        #     f.write("Contenido inicial\n")
        # print("Modo 'w': Archivo creado/sobrescrito")

        # Modo 'a' - Append (agregar al final)
        # Descomenta las siguientes líneas:
        # with open(test_modes, "a", encoding="utf-8") as f:
        #     f.write("Contenido agregado\n")
        # print("Modo 'a': Contenido agregado al final")

        # Ver resultado
        # Descomenta las siguientes líneas:
        # print("Contenido final:")
        # print(test_modes.read_text(encoding="utf-8"))

        # Modo 'x' - Creación exclusiva
        # Descomenta las siguientes líneas:
        # try:
        #     with open(test_modes, "x", encoding="utf-8") as f:
        #         f.write("Esto fallará")
        # except FileExistsError:
        #     print("Modo 'x': FileExistsError - El archivo ya existe!")

        # ============================================
        # PASO 5: Trabajando con pathlib
        # ============================================
        print("\n--- Paso 5: pathlib ---")

        # Crear estructura de directorios
        # Descomenta las siguientes líneas:
        # data_dir = work_dir / "data" / "processed"
        # data_dir.mkdir(parents=True, exist_ok=True)
        # print(f"Directorio creado: {data_dir}")

        # Crear archivo en subdirectorio
        # Descomenta las siguientes líneas:
        # data_file = data_dir / "resultado.txt"
        # data_file.write_text("Datos procesados", encoding="utf-8")

        # Propiedades de Path
        # Descomenta las siguientes líneas:
        # print(f"Nombre: {data_file.name}")
        # print(f"Stem: {data_file.stem}")
        # print(f"Sufijo: {data_file.suffix}")
        # print(f"Padre: {data_file.parent}")
        # print(f"Existe: {data_file.exists()}")
        # print(f"Es archivo: {data_file.is_file()}")

        # Listar archivos
        # Descomenta las siguientes líneas:
        # print("\nArchivos .txt en work_dir:")
        # for txt_file in work_dir.glob("**/*.txt"):
        #     print(f"  - {txt_file.relative_to(work_dir)}")

        # ============================================
        # PASO 6: Archivos CSV
        # ============================================
        print("\n--- Paso 6: Archivos CSV ---")

        # Crear CSV de prueba
        csv_file = work_dir / "usuarios.csv"
        # Descomenta las siguientes líneas:
        # with open(csv_file, "w", encoding="utf-8", newline="") as f:
        #     writer = csv.DictWriter(f, fieldnames=["nombre", "email", "edad"])
        #     writer.writeheader()
        #     writer.writerows([
        #         {"nombre": "Ana García", "email": "ana@example.com", "edad": "28"},
        #         {"nombre": "Carlos López", "email": "carlos@example.com", "edad": "35"},
        #         {"nombre": "María Rodríguez", "email": "maria@example.com", "edad": "42"},
        #     ])
        # print("CSV creado: usuarios.csv")

        # Leer CSV como diccionarios
        # Descomenta las siguientes líneas:
        # print("\nLeyendo CSV:")
        # with open(csv_file, "r", encoding="utf-8", newline="") as f:
        #     reader = csv.DictReader(f)
        #     for row in reader:
        #         print(f"  {row['nombre']} ({row['edad']} años): {row['email']}")

        # ============================================
        # PASO 7: Archivos JSON
        # ============================================
        print("\n--- Paso 7: Archivos JSON ---")

        # Datos de configuración
        config = {
            "app_name": "Mi Aplicación",
            "version": "1.0.0",
            "settings": {
                "theme": "dark",
                "language": "es",
                "notifications": True
            },
            "users": ["admin", "guest"]
        }

        json_file = work_dir / "config.json"

        # Escribir JSON
        # Descomenta las siguientes líneas:
        # with open(json_file, "w", encoding="utf-8") as f:
        #     json.dump(config, f, indent=2, ensure_ascii=False)
        # print("JSON escrito: config.json")

        # Leer JSON
        # Descomenta las siguientes líneas:
        # with open(json_file, "r", encoding="utf-8") as f:
        #     loaded_config = json.load(f)
        # print(f"\nConfiguración cargada:")
        # print(f"  App: {loaded_config['app_name']}")
        # print(f"  Tema: {loaded_config['settings']['theme']}")
        # print(f"  Usuarios: {', '.join(loaded_config['users'])}")

        # ============================================
        # PASO 8: Ejercicio Integrador
        # ============================================
        print("\n--- Paso 8: Ejercicio Integrador ---")

        # Crea una función que procese un archivo de texto
        # y genere estadísticas

        # Descomenta las siguientes líneas:
        # def analyze_text_file(file_path: Path) -> dict[str, int]:
        #     """
        #     Analiza un archivo de texto y retorna estadísticas.
        #
        #     Returns:
        #         dict con lines, words, characters
        #     """
        #     stats = {"lines": 0, "words": 0, "characters": 0}
        #
        #     with open(file_path, "r", encoding="utf-8") as f:
        #         for line in f:
        #             stats["lines"] += 1
        #             stats["words"] += len(line.split())
        #             stats["characters"] += len(line)
        #
        #     return stats
        #
        # # Probar la función
        # stats = analyze_text_file(multi_line)
        # print(f"Estadísticas de {multi_line.name}:")
        # print(f"  Líneas: {stats['lines']}")
        # print(f"  Palabras: {stats['words']}")
        # print(f"  Caracteres: {stats['characters']}")

    print("\n" + "=" * 60)
    print("¡Ejercicio completado!")
    print("=" * 60)


if __name__ == "__main__":
    main()

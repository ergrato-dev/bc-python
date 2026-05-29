# Glosario — Semana 22: Automatización del Sistema de Archivos

## pathlib

**Path**
Objeto que representa una ruta del sistema de archivos. Inmutable. Soporta operadores `/` para concatenar segmentos. Reemplaza a `os.path` con una API orientada a objetos.

**glob(pattern)**
Método de `Path` que busca archivos en el directorio actual usando patrones shell (`*`, `?`, `[...]`). No recursivo por defecto.

**rglob(pattern)**
Equivalente a `glob("**/pattern")`. Busca recursivamente en todo el árbol de subdirectorios.

**stem / suffix / name**
Componentes del nombre de archivo. `name = stem + suffix`. Ej: `"spot.mp4"` → `stem="spot"`, `suffix=".mp4"`, `name="spot.mp4"`.

**Path.stat()**
Retorna un `os.stat_result` con metadatos del archivo: `st_size` (bytes), `st_mtime` (unix timestamp de última modificación), `st_ctime` (cambio de metadata).

---

## watchdog

**Observer**
Hilo daemon de watchdog que escucha al SO por cambios en el filesystem. Se inicia con `observer.start()` y se detiene con `observer.stop()` + `observer.join()`.

**FileSystemEventHandler**
Clase base con métodos `on_created`, `on_modified`, `on_deleted`, `on_moved`. Sobreescribir solo los eventos necesarios.

**PatternMatchingEventHandler**
Subclase de `FileSystemEventHandler` que filtra eventos por patrones glob antes de despacharlos. Útil para reaccionar solo a `.mp4` o `*.wav`.

**FileCreatedEvent / FileMovedEvent**
Clases de evento. `src_path` en todos. `FileMovedEvent` también tiene `dest_path`. `event.is_directory` distingue archivo de carpeta.

**inotify**
Subsistema del kernel Linux que notifica cambios en el filesystem. watchdog lo usa internamente. Tiene un límite de `max_user_watches` (por defecto 8192 en muchas distros).

---

## Checksums e Idempotencia

**Checksum**
Valor hash calculado sobre el contenido de un archivo. Permite verificar integridad (el contenido no cambió) y detectar duplicados (mismo contenido = mismo hash).

**SHA-256**
Función hash criptográfica que produce un digest de 256 bits (64 caracteres hex). Sin colisiones conocidas. Estándar para checksums de producción.

**MD5**
Función hash más rápida que SHA-256. Vulnerable a colisiones intencionales. Aceptable para checksums de integridad donde el adversario no controla el contenido.

**Idempotencia**
Propiedad de una operación que puede aplicarse múltiples veces sin cambiar el resultado más allá de la primera aplicación. Un pipeline idempotente produce el mismo estado final aunque se ejecute 5 veces.

**Registro de procesados**
Archivo JSON que mapea `{checksum: dest_path}`. Persiste entre ejecuciones del daemon para garantizar idempotencia tras reinicios.

---

## Organización y Nomenclatura

**Naming convention**
Reglas formales para nombrar archivos: qué componentes incluir, en qué orden, qué separadores usar. Permite parsear metadata del nombre sin consultar bases de datos.

**Slug**
Representación de texto libre en formato URL-friendly: minúscula, sin espacios, solo alfanumérico y guiones. Ej: `"Spot Verano 2024"` → `"spot-verano-2024"`.

**Operación atómica**
Operación que no puede observarse en un estado intermedio. En filesystems: `rename()` dentro del mismo dispositivo es atómica — nunca hay un archivo a medias entre origen y destino.

**Cross-device move**
Movimiento entre dispositivos distintos (ej: disco interno → NAS). `Path.rename()` falla; `shutil.move()` lo maneja copiando y luego borrando.

**Lock file**
Archivo que indica que un proceso está activo. Contiene el PID. Permite detectar si el daemon ya corre antes de lanzar una segunda instancia.

---

## Patrones de Diseño

**Daemon**
Proceso de larga duración que corre en segundo plano, reaccionando a eventos. No interactivo. Se inicia, monitorea, y se detiene con señal (SIGINT, Ctrl+C).

**Pipeline de ingest**
Secuencia de pasos para incorporar archivos externos al sistema: recibir → validar → clasificar → normalizar → almacenar → registrar.

**Event-driven**
Paradigma donde el flujo de ejecución está determinado por eventos externos (creación de archivo, llegada de mensaje) en lugar de secuencia predefinida.

# Glosario — Semana 23: Procesamiento de Imágenes

## Pillow y formatos

**PIL / Pillow**
Python Imaging Library. `PIL` es el nombre histórico; `Pillow` es el fork activo desde 2010. Se importa como `from PIL import Image` aunque el paquete se instala como `pillow`.

**Image.open()**
Abre un archivo de imagen en modo lazy — no carga los píxeles hasta que se accede a ellos. Siempre usar como context manager (`with Image.open() as img`) para liberar el archivo.

**Image.thumbnail()**
Reduce una imagen in-place para que quepa en el bounding box dado, preservando proporciones. Nunca agranda. Modifica el objeto directamente — hacer `img.copy()` antes si se necesita el original.

**ImageOps.fit()**
Redimensiona y recorta una imagen para llenar exactamente las dimensiones indicadas. Útil para thumbnails cuadrados de redes sociales.

**LANCZOS**
Filtro de remuestreo de alta calidad. `Image.LANCZOS` (también `Image.Resampling.LANCZOS` en Pillow 10+). Más lento que BILINEAR pero produce imágenes más nítidas sin artefactos.

**ImageOps.exif_transpose()**
Corrige la orientación de una imagen según sus metadatos EXIF. Necesario porque las cámaras almacenan la rotación en EXIF sin girar los píxeles.

---

## Modos de color

**RGB**
Tres canales (Rojo, Verde, Azul), 8 bits cada uno. Modo estándar para fotos en pantalla. JPG solo acepta RGB.

**RGBA**
RGB + canal Alpha (transparencia), 8 bits cada uno. Necesario para PNG con transparencia y para alpha compositing.

**L (Luminosity)**
Un solo canal de 8 bits representando luminosidad. Equivale a escala de grises. Útil como máscara en operaciones de compositing.

**CMYK**
Cuatro canales para impresión: Cyan, Magenta, Yellow, Key (negro). Los monitores no reproducen CMYK con precisión — usar solo para workflows de impresión.

---

## Formatos

**JPG / JPEG**
Compresión con pérdida. No soporta transparencia. `quality` de 85-90 es el rango profesional. Progresivo mejora la carga web.

**PNG**
Compresión sin pérdida. Soporta RGBA. Ideal para gráficos con transparencia, logos, capturas de pantalla.

**WebP**
Formato moderno de Google. Soporta compresión con y sin pérdida, y transparencia. 25-35% más pequeño que JPG a misma calidad visual.

**TIFF**
Formato de archivo sin pérdida. Soporta múltiples capas y alta profundidad de color. Estándar en producción fotográfica y pre-impresión.

**RAW**
Datos crudos del sensor de la cámara (CR2, NEF, ARW). No es un formato de imagen estándar — requiere `rawpy` para decodificar. Mayor rango dinámico que JPG.

---

## Compositing y watermarks

**Alpha compositing**
Técnica para combinar dos imágenes usando un canal de transparencia (alpha). `Image.paste(src, pos, mask)` aplica compositing: píxeles con alpha=255 son opacos, alpha=0 son transparentes.

**`Image.paste(img, pos, mask)`**
Pega `img` sobre `self` en la posición `pos`. El tercer argumento es la máscara de alpha: si es un objeto Image en modo L o RGBA, controla la transparencia píxel a píxel.

**`Image.alpha_composite()`**
Combina dos imágenes RGBA aplicando compositing sobre-bajo (Porter-Duff). Más preciso que `paste()` para overlays complejos.

**ImageDraw**
Módulo de Pillow para dibujar formas y texto sobre una imagen. `ImageDraw.Draw(img)` retorna un contexto de dibujo. Las operaciones son in-place sobre `img`.

**`draw.textbbox()`**
Retorna el bounding box `(left, top, right, bottom)` de un texto dado con fuente dada. Necesario para centrar texto correctamente.

---

## Batch processing

**ThreadPoolExecutor**
Ejecuta funciones en múltiples hilos. Para procesamiento de imágenes: libera el GIL durante I/O de disco y durante operaciones de compresión de Pillow (implementadas en C).

**`as_completed(futures)`**
Iterador que retorna futuros a medida que se completan (no en orden de envío). Permite actualizar una barra de progreso en tiempo real.

**`img.verify()`**
Verifica la cabecera del archivo sin cargar los píxeles. Detecta imágenes corruptas. Tras `verify()`, el objeto Image queda inutilizable — reabrirlo antes de procesar.

**EXIF**
Exchangeable Image File Format. Metadatos embebidos en JPG/TIFF por cámaras digitales: fecha, ISO, apertura, GPS, modelo de cámara. `piexif` permite leerlos y escribirlos.

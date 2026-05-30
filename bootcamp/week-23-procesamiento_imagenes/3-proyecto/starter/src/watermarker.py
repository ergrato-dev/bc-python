"""Aplicación de watermarks: logo y texto."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


def apply_logo(
    base: Image.Image,
    logo_path: Path,
    corner: str = "bottom-right",
    margin: int = 20,
    max_ratio: float = 0.12,
) -> Image.Image:
    """
    Aplica logo PNG en la esquina indicada.
    Retorna nueva imagen con logo; no modifica base.
    """
    # TODO:
    # 1. logo = Image.open(logo_path).convert("RGBA")
    # 2. Escalar logo si es mayor que max_ratio * base.width
    # 3. result = base.copy().convert("RGBA")
    # 4. Calcular posición según corner y margin
    # 5. result.paste(logo, pos, mask=logo)
    # 6. return result.convert("RGB")
    raise NotImplementedError


def apply_text(
    base: Image.Image,
    text: str = "© Studio BC",
    opacity: int = 70,
    font_size: int = 28,
) -> Image.Image:
    """
    Agrega texto semitransparente centrado en la parte inferior.
    Retorna nueva imagen; no modifica base.
    """
    # TODO:
    # 1. result = base.convert("RGBA")
    # 2. overlay = Image.new("RGBA", result.size, (0,0,0,0))
    # 3. draw = ImageDraw.Draw(overlay)
    # 4. Cargar fuente o usar load_default()
    # 5. Centrar texto horizontalmente, posicionar a 90% del alto
    # 6. draw.text(pos, text, font=font, fill=(255,255,255,opacity))
    # 7. result = Image.alpha_composite(result, overlay)
    # 8. return result.convert("RGB")
    raise NotImplementedError

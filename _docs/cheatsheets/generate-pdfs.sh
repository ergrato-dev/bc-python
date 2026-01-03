#!/bin/bash
# Script para generar PDFs de los Cheat Sheets con formato profesional
# Uso: ./generate-pdfs.sh
# Requisitos: pandoc, texlive-scheme-basic, texlive-collection-latexextra

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR" || exit

echo "📄 Generando PDFs de los Cheat Sheets..."
echo "=========================================="

# Lista de archivos a convertir (excluir README.md)
FILES=(
    "python-basics.md"
    "data-structures.md"
    "oop-python.md"
    "file-handling.md"
    "testing-debugging.md"
    "complete-reference.md"
)

# Caracteres a remover (emojis y símbolos especiales que LaTeX no soporta)
CHARS_TO_REMOVE='[📋📑✅❌⚠️🔥💡🎯📌🐍💻🔧📊📁🚀✨🔹🔸▶️🎉📝🔍📖💾🌐🔐📦🛠️⚙️🔬📐📈📉🎨🔔🕐💪🧠🧩🌟⭐💎🔗📚✏️🖥️💻⌨️🖱️📱🗂️📂🗃️🗄️├└│─]'

# Opciones de Pandoc para mejor formato
PANDOC_OPTS=(
    --pdf-engine=pdflatex
    --toc
    --toc-depth=2
    -V geometry:margin=2cm
    -V fontsize=10pt
    -V documentclass=article
    -V papersize=a4
    -V colorlinks=true
    -V linkcolor=blue
    -V urlcolor=blue
    --highlight-style=tango
)

# Contador de éxitos/errores
SUCCESS=0
FAILED=0

# Crear directorio temporal
TEMP_DIR=$(mktemp -d)
trap 'rm -rf "$TEMP_DIR"' EXIT

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        output="${file%.md}.pdf"
        temp_file="$TEMP_DIR/${file}"
        
        echo -n "📝 Convirtiendo $file -> $output... "
        
        # Crear versión sin emojis en archivo temporal
        sed "s/$CHARS_TO_REMOVE//g" "$file" > "$temp_file"
        
        if pandoc "$temp_file" -o "$output" "${PANDOC_OPTS[@]}" 2>/dev/null; then
            echo "✅"
            SUCCESS=$((SUCCESS + 1))
        else
            echo "❌"
            FAILED=$((FAILED + 1))
        fi
    else
        echo "⚠️  Archivo no encontrado: $file"
        FAILED=$((FAILED + 1))
    fi
done

echo ""
echo "=========================================="
echo "✅ Completado: $SUCCESS PDFs generados"
if [ $FAILED -gt 0 ]; then
    echo "❌ Errores: $FAILED"
fi
echo ""
echo "📁 PDFs generados en: $SCRIPT_DIR"
ls -lh *.pdf 2>/dev/null || echo "No se encontraron PDFs"

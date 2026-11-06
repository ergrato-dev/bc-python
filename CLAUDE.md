# bc-python

Bootcamp Python de cero a avanzado, con énfasis en data science e IA. 42 semanas x 18 h = 756 h. Molde: `../bc-android-kotlin`. Plan aprobado: `~/.claude/plans/elegant-coalescing-dusk.md`.

Reglas duras:
- 18 h por semana: la tabla de tiempos de cada README de semana suma exactamente 18 h; si suma más, se recorta alcance.
- Tuteo siempre, nunca voseo. Prosa en español; código, identificadores, nombres técnicos y commits en inglés (Conventional Commits).
- `uv` siempre, nunca `pip`. `pnpm` siempre, nunca `npm`. PostgreSQL siempre, nunca MySQL.
- Docker donde haga falta un servicio o reproducibilidad: `Dockerfile` multi-stage con imagen `uv` pinada y `compose.yaml`.
- Versiones completas pinadas, nunca `latest`; verificar tag y CVEs antes de fijar (`docs/stack-versions.md`, con fecha y fuente).
- Carpeta de semana: `week-NN-slug_snake_case/{README.md,rubrica-evaluacion.md,0-assets,1-teoria,2-practicas,3-proyecto,4-recursos,5-glosario}`.
- Prácticas: `2-practicas/ejercicio-NN-slug/{README.md,starter/}`. Sin `solution/`. Starter con `pyproject.toml` + `uv.lock`; `uv run pytest` arranca en rojo y termina en verde.
- Ejercicios paso a paso, sin dar nada por sabido: comando exacto, salida esperada y tabla "🧯 Si algo sale mal".
- Comentarios de código: qué / para qué / impacto, solo donde aportan, sin repetirse.
- SVG según necesidad real de la teoría; cada SVG se referencia desde una teoría.
- Todo `.md` de semana termina con tabla `## 🔗 Navegación` (Anterior | Actual | Siguiente).
- Rúbrica 30/40/30 (conocimiento/desempeño/producto), mínimo 70% por evidencia.
- Dominios por aprendiz (`docs/dominios.md`); un proyecto hilo conductor (`docs/proyecto-hilo-conductor.md`).
- Una semana por tanda, un commit por semana. El contenido de la versión anterior (36 semanas) vive en el tag `legacy-36w`.
- Antes de cada commit: `./scripts/verificar-enlaces.sh` en verde. Al publicar una semana, marcarla ✅ en `bootcamp/README.md`.

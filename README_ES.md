<p align="center">
  <a href="README.md">简体中文</a> ·
  <a href="README_EN.md">English</a> ·
  <a href="README_JA.md">日本語</a> ·
  <a href="README_KO.md">한국어</a> ·
  <a href="README_PT-BR.md">Português do Brasil</a> ·
  <b>Español</b> ·
  <a href="README_ID.md">Bahasa Indonesia</a>
</p>

# Manual de Entrevistas para Ingeniería de IA

> Una guía estructurada para puestos de aplicaciones de IA, RAG, agentes, entrenamiento e inferencia de modelos, FDE, multimodalidad y seguridad de IA.

**619 preguntas · 28 temas · 7 rutas profesionales**

> [!IMPORTANT]
> Esta página es una traducción de la presentación del proyecto. El banco completo de preguntas y respuestas se mantiene actualmente en chino simplificado. Los enlaces siguientes abren el contenido en chino.

## Por qué usar este repositorio

- **Orientado a puestos reales:** cubre capacidades recurrentes en empleos de ingeniería de IA, no solo preguntas aisladas.
- **Decisiones de ingeniería primero:** analiza calidad, latencia, coste, seguridad, complejidad y alternativas.
- **Calidad verificable:** las auditorías detectan enlaces rotos, preguntas duplicadas, métricas precisas sin fuente y la cobertura 1:1 entre preguntas e ilustraciones.

## Aprendizaje visual

Los 28 temas y las 619 preguntas incluyen ahora una ilustración didáctica 16:9 dedicada y ampliable. Cada imagen resume mecanismos, flujos, decisiones, límites y una frase para recordar. Las etiquetas se mantienen en chino, como el banco de preguntas original, pero los términos técnicos y el flujo visual siguen siendo reconocibles.

<table>
  <tr>
    <td width="33%" align="center"><a href="docs/01-basic-concepts/"><img src="assets/illustrations/01-basic-concepts/q25-kv-cache.webp" width="100%" alt="Ilustración de fundamentos de LLM: KV Cache"></a><br><b>Fundamentos de LLM</b></td>
    <td width="33%" align="center"><a href="docs/03-rag-system/"><img src="assets/illustrations/03-rag-system/q02-rag-pipeline.webp" width="100%" alt="Ilustración de RAG: pipeline de producción"></a><br><b>Sistemas RAG</b></td>
    <td width="33%" align="center"><a href="docs/04-transformer-architecture/"><img src="assets/illustrations/04-transformer-architecture/q03-self-attention.webp" width="100%" alt="Ilustración de Transformer: mecanismo de Self-Attention"></a><br><b>Transformer</b></td>
  </tr>
  <tr>
    <td width="33%" align="center"><a href="docs/05-ai-agent-basics/"><img src="assets/illustrations/05-ai-agent-basics/q02-react-loop.webp" width="100%" alt="Ilustración de agentes: ciclo de razonamiento y acción ReAct"></a><br><b>Agentes de IA</b></td>
    <td width="33%" align="center"><a href="docs/08-inference-optimization/"><img src="assets/illustrations/08-inference-optimization/q05-pagedattention.webp" width="100%" alt="Ilustración de inferencia: gestión de memoria con PagedAttention"></a><br><b>Entrenamiento e Inferencia</b></td>
    <td width="33%" align="center"><a href="docs/10-production-deployment/"><img src="assets/illustrations/10-production-deployment/q12-llm-gateway.webp" width="100%" alt="Ilustración de IA en producción: arquitectura de LLM Gateway"></a><br><b>Seguridad y Producción</b></td>
  </tr>
</table>

<p align="center"><b>28 temas · 619 preguntas · cobertura completa de una ilustración por pregunta</b></p>

## Elige tu ruta

| Puesto | Ruta recomendada |
|---|---|
| Ingeniería de Aplicaciones de IA / LLM | [Fundamentos de LLM](docs/01-basic-concepts/) → [Prompt Engineering](docs/02-prompt-engineering/) → [RAG](docs/03-rag-system/) → [Agentes](docs/05-ai-agent-basics/) → [Producción](docs/10-production-deployment/) → [Diseño de Sistemas de IA](docs/25-system-design-ai/) |
| Ingeniería de RAG | [Fundamentos de LLM](docs/01-basic-concepts/) → [RAG](docs/03-rag-system/) → [Búsqueda Vectorial](docs/06-vector-index-optimization/) → [RAG Avanzado](docs/20-rag-advanced-optimization/) → [Seguridad y Evaluación](docs/09-ai-safety-evaluation/) → [Observabilidad](docs/23-agent-observability/) |
| Ingeniería de Agentes | [Prompt Engineering](docs/02-prompt-engineering/) → [Agentes](docs/05-ai-agent-basics/) → [Planificación y Reflexión](docs/22-agent-planning-reflection/) → [Multi-Agent](docs/13-multi-agent-systems/) → [MCP y Skills](docs/14-mcp-skill-systems/) → [Observabilidad](docs/23-agent-observability/) |
| Ingeniería de Entrenamiento e Inferencia | [Transformer](docs/04-transformer-architecture/) → [Entrenamiento](docs/07-model-training/) → [Optimización de Inferencia](docs/08-inference-optimization/) → [Frameworks de Inferencia](docs/19-inference-frameworks/) |
| Forward Deployed Engineer | [Proyectos en Profundidad](docs/27-project-experience/) → [Ingeniería con Python](docs/24-python-engineering/) → [Diseño de Sistemas de IA](docs/25-system-design-ai/) → [FDE](docs/26-forward-deployed-engineer/) |
| Ingeniería de IA Multimodal | [Transformer](docs/04-transformer-architecture/) → [IA Multimodal](docs/11-multimodal-ai/) → [Agentes Multimodales](docs/21-multimodal-agents/) → [Producción](docs/10-production-deployment/) |
| Ingeniería de Seguridad y Evaluación | [Fundamentos de LLM](docs/01-basic-concepts/) → [Prompt Engineering](docs/02-prompt-engineering/) → [Seguridad y Evaluación](docs/09-ai-safety-evaluation/) → [Test Harness y Evaluación](docs/28-test-harness-evaluation/) → [Observabilidad](docs/23-agent-observability/) → [Producción](docs/10-production-deployment/) |

## Mapa de temas

- **Fundamentos y modelos:** LLM, Transformer, entrenamiento, optimización y frameworks de inferencia.
- **RAG y recuperación:** sistemas RAG, índices vectoriales y RAG avanzado en producción.
- **Agentes y protocolos:** fundamentos de agentes, Multi-Agent, MCP/Skills, planificación y observabilidad.
- **Ingeniería y diseño de sistemas:** seguridad, producción, Python, diseño de sistemas de IA, FDE y [Test Harness y Evaluación](docs/28-test-harness-evaluation/).
- **Multimodalidad y temas emergentes:** IA multimodal, herramientas de programación con IA y temas avanzados.
- **Preparación de entrevistas:** currículum, fuentes de entrevistas y análisis de proyectos.

Consulta el [catálogo completo en el README chino](README.md#catalog).

## Cómo practicar

Prepara tres versiones de cada respuesta:

1. **30 segundos:** presenta la decisión y el razonamiento principal.
2. **3 minutos:** explica principios, alternativas y compromisos.
3. **Profundización:** explica cómo validar, gestionar fallos y por qué descartaste otra opción.

Sustituye todas las métricas de ejemplo por evidencia de tu propio trabajo. El comportamiento de productos, precios y benchmarks puede cambiar; comprueba los datos temporales en documentación oficial o artículos originales.

## Contribuir

Lee la [política de calidad del contenido](CONTENT_QUALITY.md) antes de modificar preguntas. Las mejoras de traducción son bienvenidas. Hasta que exista una traducción completa con mantenimiento continuo, el banco chino será la fuente oficial.

Abre un [Issue](https://github.com/guocong-bincai/ai-interview-guide/issues) para informar de un problema o envía un [Pull Request](https://github.com/guocong-bincai/ai-interview-guide/pulls) con una corrección.

## Licencia

[MIT](LICENSE)

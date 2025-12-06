---
description: Optimiza un prompt para Claude Opus 4.5 aplicando mejores prácticas oficiales de Anthropic
argument-hint: "[prompt a optimizar o @archivo.md]"
---

# Prompt Optimizer para Claude Opus 4.5 (Django/FastAPI Context)

## PASO 0: Delegación a Agente Especializado (OBLIGATORIO)

**ANTES de hacer cualquier otra cosa**, analiza el prompt a optimizar y delega al agente especializado correspondiente.

### Prompt Recibido
```
$ARGUMENTS
```

### Matriz de Detección — Ejecuta AHORA

| Si el prompt contiene... | INVOCA INMEDIATAMENTE |
|--------------------------|----------------------|
| Django, modelo, view, template, ORM, admin, migration | → `Task(subagent_type="django-architect")` |
| FastAPI, endpoint, Pydantic, async, router, microservicio | → `Task(subagent_type="django-architect")` |
| CSS, tokens, diseño, UI, Sacred Geometry, componente visual | → `Task(subagent_type="frontend-artist")` |
| seguridad, OWASP, headers, SSL, firewall, auth, CSRF | → `Task(subagent_type="security-auditor")` |
| test, pytest, coverage, TDD, mock, fixture | → `Task(subagent_type="croody-tester")` |
| Docker, nginx, deploy, AWS, Terraform, infraestructura | → `Task(subagent_type="sysadmin-ops")` |
| documentación, docs, ADR, Diátaxis, README | → `Task(subagent_type="doc-guardian")` |
| arquitectura, explorar código, cómo funciona | → `Task(subagent_type="code-explorer")` |

### Acción Requerida

**SI detectas match en la matriz:**
```
USA Task tool AHORA con:
- subagent_type: "[agente-de-la-matriz]"
- prompt: "Optimiza este system prompt para Croody Web aplicando:
          1. Principios de Claude Opus 4.5 (claridad, tono calibrado, anti-overengineering)
          2. Tu expertise especializada en [dominio del agente]
          3. Contexto específico de Croody (Django, FastAPI, Sacred Geometry)

          Prompt a optimizar:
          [CONTENIDO DE $ARGUMENTS]

          Entrega el prompt optimizado con análisis de cambios realizados."
```

**SI NO hay match claro** → Continúa con el proceso manual a continuación.

---

> **Fuente:** [Claude 4 Best Practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-4-best-practices)

## Características de Opus 4.5 (Contexto)

Antes de optimizar, considera estas características específicas del modelo:

| Característica | Impacto en Prompting |
|----------------|----------------------|
| **Más responsivo al system prompt** | Puede "overtrigger" en tools si el lenguaje es agresivo |
| **Tendencia a sobreingenierar** | Requiere restricciones explícitas |
| **Effort Parameter exclusivo** | Controla tokens (high/medium/low) |
| **Sensible a "think"** | Usar "consider", "evaluate", "assess" en su lugar |
| **Directo y conciso** | Prefiere instrucciones explícitas sobre implícitas |

---

## Principios de Optimización (Documentación Oficial)

Aplica cada principio sistemáticamente:

### 1. Sé Claro y Directo

Claude 4.x requiere dirección explícita. Evita ambigüedad.

> "Think of Claude as a brilliant but newly hired employee with no memory of your workplace norms."
> — [Be Clear and Direct](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/be-clear-and-direct)

**Transforma:**
| Vago | Específico |
|------|------------|
| "Mejora esto" | "Refactoriza esta view para usar CBV en lugar de FBV" |
| "Hazlo mejor" | "Optimiza la query para evitar N+1 usando select_related" |
| "Podrías..." | "Implementa..." |

### 2. Calibra el Tono (Sin Lenguaje Agresivo)

Opus 4.5 responde mejor a "normal prompting" que a énfasis agresivo.

> "If your prompts were designed to reduce undertriggering... Claude Opus 4.5 may now overtrigger. The fix is to dial back any aggressive language."
> — [Claude 4 Best Practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-4-best-practices)

**Transforma:**
| Agresivo | Normal |
|----------|--------|
| `NEVER do X` | `Evita X porque [razón]` |
| `YOU MUST always` | `Asegúrate de...` |
| `CRITICAL:`, `IMPORTANT:` | Integrar en prosa normal |
| `DO NOT` | `Evita...` |
| MAYÚSCULAS | **Negritas** si necesitas énfasis |

### 3. Fuerza la Acción Explícitamente

Claude 4.x puede preferir sugerir en lugar de implementar. Usa frases explícitas.

> "Say 'Change this function to improve its performance' rather than 'Can you suggest some changes?'"
> — [Claude 4 Best Practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-4-best-practices)

**Incluye una de estas frases:**
- "Implementa los cambios directamente, no solo los sugieras."
- "Escribe código funcional que pueda ejecutarse."
- "Realiza las modificaciones en los archivos."
- "Por defecto, implementa en lugar de solo recomendar."

### 4. Contén la Sobre-Ingeniería

Opus 4.5 tiende a crear abstracciones innecesarias.

> "Claude Opus 4.5 has a tendency to overengineer by creating extra files, adding unnecessary abstractions, or building in flexibility that wasn't requested."
> — [Claude 4 Best Practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-4-best-practices)

**Incluye restricciones:**
```
Mantén la solución simple y enfocada. No agregues features, refactors,
ni abstracciones más allá de lo solicitado. Un bug fix no necesita
limpiar código circundante. Una feature simple no necesita configurabilidad extra.

Fat model pattern: lógica en modelo, no en vista.
Modifica archivos in-situ, no crees helpers nuevos.
```

### 5. Justifica las Reglas (El Por Qué)

Contexto mejora cumplimiento y reduce "malicious compliance".

> "Context Matters: Explain the *why* behind requests."
> — [Claude 4 Best Practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-4-best-practices)

**Estructura:** `Haz X porque [razón técnica/negocio].`

**Ejemplo:**
```diff
- "Usa tokens CSS"
+ "Usa tokens CSS (var(--brand-base)) porque mantiene consistencia con Sacred Geometry"
```

### 6. Evita la Palabra "Think"

Opus 4.5 es sensible a "think" cuando extended thinking está deshabilitado.

> "When extended thinking is disabled, Claude Opus 4.5 responds better to alternatives like 'consider,' 'believe,' or 'evaluate.'"
> — [Claude 4 Best Practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-4-best-practices)

**Transforma:**
| Evitar | Usar |
|--------|------|
| "Think about..." | "Consider..." |
| "Think through..." | "Evaluate..." |
| "Let me think" | "Let me assess" |
| "Think step by step" | "Reason through this step by step" |

### 7. Estructura con XML Tags

XML tags mejoran claridad y parseabilidad.

> "XML tags structure prompts by separating components like context, instructions, and examples. This improves clarity, reduces misinterpretation, and enhances output quality."
> — [Use XML Tags](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/use-xml-tags)

**Estructura recomendada:**
```xml
<context>
[Información de fondo relevante]
</context>

<instructions>
[Lo que debe hacer específicamente]
</instructions>

<constraints>
[Límites y restricciones]
</constraints>

<output_format>
[Formato esperado del resultado]
</output_format>
```

### 8. Incluye Ejemplos (Si Aplica)

2-3 ejemplos reducen malinterpretación significativamente.

> "Include 3-5 diverse, relevant examples to show Claude exactly what you want."
> — [Multishot Prompting](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/multishot-prompting)

**Estructura:**
```xml
<examples>
<example>
<input>[Entrada de ejemplo]</input>
<output>[Salida esperada]</output>
</example>
</examples>
```

---

## Modo de Acción vs Modo Conservador

### Modo Acción (Default para implementación)
```
Implementa los cambios directamente. Por defecto, realiza modificaciones
en lugar de solo sugerirlas.
```

### Modo Conservador (Para investigación/análisis)
```
No saltes a la implementación ni cambies archivos a menos que se indique claramente.
Cuando la intención sea ambigua, proporciona información e investigación en lugar de actuar.
```

---

## Detección de Contexto: Croody Web

### Si es UI/Diseño

**Cuando el prompt menciona CSS, templates, componentes visuales:**

Invoca el skill sacred-geometry-design para garantizar adherencia al sistema de diseño:
```
skill: "sacred-geometry-design"
```

**Reemplaza adjetivos genéricos:**
| Genérico | Croody-Specific |
|----------|-----------------|
| "moderno" | "Dark theme con surface layers" |
| "minimalista" | "Functional UI zone (LOW expressivity)" |
| "colorido" | "Gator palette tokens" |
| "animado" | "233ms transition, spring ease" |
| "premium" | "Vector card con shimmer hover" |

**Restricciones de diseño Croody:**
- Usa tokens de `tokens.css`, nunca colores hardcodeados
- Border radius: var(--radius-2) para botones, var(--radius-3) para cards
- Glows solo en featured products y celebrations (HIGH zone)
- Spacing: Fibonacci (8, 13, 21, 34, 55, 89px)
- Timing: 233ms base (φ-derived)

### Si es Backend (Django/FastAPI)

**Cuando el prompt menciona modelos, vistas, APIs:**

Invoca el skill django-patterns:
```
skill: "django-patterns"
```

**Patrones técnicos:**
- `Fat model` - lógica en modelo, no en vista
- `Thin view` - vistas solo coordinan
- `Parametrized` - queries seguras (ORM)
- `Surgical` - cambios precisos, in-situ

### Si es Seguridad

**Cuando el prompt menciona auth, headers, OWASP:**

Invoca el skill security-hardening:
```
skill: "security-hardening"
```

---

## Proceso de Optimización

1. **Detecta el contexto**: ¿UI/diseño, backend, o seguridad?

2. **Analiza** el prompt identificando:
   - Ambigüedad (principio 1)
   - Lenguaje agresivo (principio 2)
   - Falta de directivas de acción (principio 3)
   - Potencial de sobre-ingeniería (principio 4)
   - Reglas sin justificación (principio 5)
   - Uso de "think" (principio 6)
   - Oportunidad de estructurar con XML (principio 7)
   - Necesidad de ejemplos (principio 8)

3. **Transforma** aplicando cada principio

4. **Presenta** el resultado:

```markdown
## Contexto Detectado
[Backend Django | Frontend Sacred Geometry | Seguridad | Mixto]

## Análisis
| Principio | Problema | Solución |
|-----------|----------|----------|
| Claridad | [Descripción] | [Cambio] |
| Tono | [Descripción] | [Cambio] |
| ... | ... | ... |

## Prompt Optimizado

<context>
[Si aplica]
</context>

<instructions>
[El prompt transformado]
</instructions>

<constraints>
[Restricciones anti-overengineering y otras]
</constraints>

## Cambios Clave
- [Lista de cambios significativos]

## Notas
- [Sugerencias adicionales: effort parameter, extended thinking, etc.]
```

---

## Restricciones del Comando

- Mantén la intención original del prompt intacta
- Preserva código, ejemplos y especificaciones técnicas
- Si detectas UI, referencia sacred-geometry-design skill
- Si detectas backend, referencia django-patterns skill
- Si detectas seguridad, referencia security-hardening skill
- El prompt optimizado puede ser más largo si añade contexto útil
- No agregues contenido redundante

---

## Referencia Rápida

### Effort Parameter (Solo API, exclusivo Opus 4.5)
Si el prompt se usará via API y requiere análisis profundo:
- `effort: high` — Máxima thoroughness
- `effort: medium` — Balance producción/calidad
- `effort: low` — Eficiente en tokens

### Extended Thinking
Para tareas de código complejas, sugiere habilitar extended thinking si está disponible.

### Sistema de Diseño Croody (Solo si aplica)
- **Zones:** HIGH (celebrations) | MEDIUM (cards) | LOW (forms, tables)
- **Colores:** Gator (green brand), Jungle (neutrals)
- **Prohibido:** Glows en functional UI, colores hardcodeados

### Patrones Django (Solo si aplica)
- **Fat Models:** Lógica de negocio en el modelo
- **Thin Views:** Solo coordinación
- **CBV preferido:** Usar Class-Based Views
- **ORM siempre:** Nunca SQL raw

---

Ahora analiza y optimiza el prompt proporcionado.

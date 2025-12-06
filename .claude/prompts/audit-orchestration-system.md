# Prompt: Auditoría del Sistema de Orquestación

## Objetivo

Investigar documentación oficial 2025 sobre sistemas de orquestación en Claude Code y Agent SDK, luego evaluar la implementación actual del proyecto Croody Web.

---

## FASE 1: Investigación de Documentación Oficial

### 1.1 Fuentes Primarias a Consultar

Busca y extrae información de estas fuentes oficiales:

```
CLAUDE CODE (CLI):
- https://docs.anthropic.com/en/docs/claude-code
- https://docs.anthropic.com/en/docs/claude-code/sub-agents
- https://docs.anthropic.com/en/docs/claude-code/skills
- https://docs.anthropic.com/en/docs/claude-code/hooks
- https://docs.anthropic.com/en/docs/claude-code/settings

AGENT SDK:
- https://docs.anthropic.com/en/docs/agents/overview
- https://docs.anthropic.com/en/docs/agents/patterns

GUÍAS DE ANTHROPIC:
- "Building Effective Agents" (blog post 2024/2025)
- Multi-agent orchestration patterns
```

### 1.2 Términos de Búsqueda

Ejecuta búsquedas web con estos términos:

```
1. "Claude Code subagents 2025 best practices"
2. "Claude Code orchestrator pattern documentation"
3. "Anthropic multi-agent orchestration guide"
4. "Claude Code CLAUDE.md configuration guide"
5. "Claude Code agent delegation patterns"
6. "site:anthropic.com claude code agents"
7. "site:docs.anthropic.com sub-agents"
```

### 1.3 Información a Extraer

Para cada fuente, documenta:

| Aspecto | Qué Buscar |
|---------|------------|
| **Límites técnicos** | Máximo de subagentes, límites de contexto, restricciones |
| **Patrones recomendados** | Orchestrator-Workers, Routing, Parallelization |
| **Anti-patrones** | Qué evitar según documentación oficial |
| **Configuración de agentes** | Frontmatter, tools, skills, model |
| **Comunicación** | Cómo pasan información entre agentes |
| **Context management** | Cómo manejar contexto compartido |
| **Herramientas por rol** | Qué tools asignar según el rol del agente |

---

## FASE 2: Lectura de Implementación Actual

### 2.1 Archivos a Leer

```
ORQUESTADOR:
CLAUDE.md

CONTEXTO COMPARTIDO:
.claude/CROODY_CONTEXT.md

SUBAGENTES (todos):
.claude/agents/django-architect.md
.claude/agents/frontend-artist.md
.claude/agents/sysadmin-ops.md
.claude/agents/security-auditor.md
.claude/agents/croody-tester.md
.claude/agents/doc-guardian.md
.claude/agents/code-explorer.md
.claude/agents/product-manager.md

SKILLS:
.claude/skills/sacred-geometry-design/SKILL.md
.claude/skills/django-patterns/SKILL.md
.claude/skills/security-hardening/SKILL.md

HOOKS:
.claude/hooks/agent-health-check.md
```

### 2.2 Aspectos a Analizar

Para cada archivo, evalúa:

1. **Estructura del frontmatter**
   - ¿Tiene todos los campos requeridos?
   - ¿El `description` permite auto-activación?
   - ¿El `model` es apropiado para el rol?
   - ¿Los `tools` están correctamente restringidos?

2. **Claridad de rol**
   - ¿Está claro qué HACE y qué NO HACE?
   - ¿Las responsabilidades están bien delimitadas?
   - ¿Hay solapamiento con otros agentes?

3. **Protocolo de comunicación**
   - ¿Tiene formato de respuesta definido?
   - ¿Sabe cómo reportar al orquestador?
   - ¿Maneja errores correctamente?

4. **Contexto**
   - ¿Referencias a CROODY_CONTEXT.md?
   - ¿Información duplicada innecesariamente?
   - ¿Falta información crítica?

---

## FASE 3: Evaluación Comparativa

### 3.1 Checklist de Compliance

Evalúa contra documentación oficial:

```markdown
## Compliance con Documentación Oficial

### Estructura de Agentes
- [ ] Frontmatter sigue especificación oficial
- [ ] Descriptions permiten auto-activación
- [ ] Tools asignados según rol (read-only vs full)
- [ ] Model apropiado (opus/sonnet/haiku)

### Patrón de Orquestación
- [ ] Orquestador no ejecuta código (solo coordina)
- [ ] Delegación clara por matriz de intención
- [ ] Manejo de tareas complejas (multi-agente)
- [ ] Quality gates antes de reportar

### Context Management
- [ ] Contexto compartido centralizado
- [ ] Sin duplicación excesiva
- [ ] Referencias en lugar de copias

### Límites Respetados
- [ ] Número de agentes dentro del límite
- [ ] Profundidad de delegación apropiada
- [ ] Sin loops de delegación circular

### Best Practices 2025
- [ ] [Completar según hallazgos de investigación]
```

### 3.2 Análisis de Gaps

Identifica:

1. **Funcionalidades faltantes**
   - ¿Qué recomienda la documentación que no tenemos?

2. **Configuraciones incorrectas**
   - ¿Qué está mal configurado según specs oficiales?

3. **Anti-patrones detectados**
   - ¿Qué estamos haciendo que la documentación desaconseja?

4. **Oportunidades de mejora**
   - ¿Qué podríamos hacer mejor según best practices?

---

## FASE 4: Reporte Final

### Formato de Entrega

```markdown
# Auditoría del Sistema de Orquestación - Croody Web

## Resumen Ejecutivo
[2-3 párrafos con hallazgos principales]

## Documentación Consultada

| Fuente | URL | Fecha | Relevancia |
|--------|-----|-------|------------|
| [nombre] | [url] | [fecha] | [alta/media/baja] |

## Hallazgos de Documentación Oficial

### Límites y Restricciones
- [hallazgo 1]
- [hallazgo 2]

### Patrones Recomendados
- [patrón 1]: [descripción]
- [patrón 2]: [descripción]

### Anti-Patrones a Evitar
- [anti-patrón 1]: [por qué]

## Evaluación de Implementación Actual

### Fortalezas
| Aspecto | Detalle | Evidencia |
|---------|---------|-----------|
| [aspecto] | [qué está bien] | [archivo:línea] |

### Debilidades
| Aspecto | Problema | Severidad | Archivo |
|---------|----------|-----------|---------|
| [aspecto] | [descripción] | ALTO/MEDIO/BAJO | [archivo] |

### Compliance Score
- Estructura de Agentes: X/10
- Patrón de Orquestación: X/10
- Context Management: X/10
- Best Practices 2025: X/10
- **Total: X/40**

## Recomendaciones

### Críticas (Implementar inmediatamente)
1. [recomendación]
   - **Archivo:** [path]
   - **Cambio:** [descripción]
   - **Justificación:** [referencia a documentación]

### Importantes (Implementar pronto)
1. [recomendación]

### Mejoras (Nice to have)
1. [recomendación]

## Plan de Acción Sugerido

| Prioridad | Acción | Esfuerzo | Impacto |
|-----------|--------|----------|---------|
| P0 | [acción] | [bajo/medio/alto] | [descripción] |
| P1 | [acción] | [bajo/medio/alto] | [descripción] |
| P2 | [acción] | [bajo/medio/alto] | [descripción] |

## Referencias

- [URL 1]: [descripción]
- [URL 2]: [descripción]
```

---

## Instrucciones de Ejecución

```
1. INVESTIGAR primero (Fase 1)
   - Usa WebSearch para cada término de búsqueda
   - Usa WebFetch para obtener contenido de URLs oficiales
   - Documenta TODAS las fuentes consultadas

2. LEER implementación (Fase 2)
   - Lee TODOS los archivos listados
   - No asumas, lee el contenido real

3. COMPARAR (Fase 3)
   - Contrasta documentación oficial vs implementación
   - Sé objetivo y específico

4. REPORTAR (Fase 4)
   - Sigue el formato exacto
   - Incluye referencias a líneas específicas
   - Prioriza hallazgos por severidad
```

---

## Notas Importantes

- **Fecha de auditoría:** La documentación debe ser la más reciente (2025)
- **Objetividad:** Evalúa basándote en evidencia, no en suposiciones
- **Especificidad:** Cita archivos y líneas específicas
- **Actionable:** Las recomendaciones deben ser implementables

---

## Contexto del Proyecto

Este audit será usado en el proyecto **Croody Web** que tiene:
- 8 subagentes especializados (django-architect, frontend-artist, sysadmin-ops, etc.)
- 3 skills (sacred-geometry-design, django-patterns, security-hardening)
- Varios slash commands (/clarify, /test-generate, /security-audit, etc.)
- Hooks de health check
- Arquitectura Django + FastAPI + Docker

El objetivo es verificar que la configuración sigue best practices oficiales de Anthropic.

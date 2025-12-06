# Meta-Prompt: Crear Subagente Experto en Claude Code

## Objetivo

Generar un archivo de subagente (`.claude/agents/claude-code-expert.md`) que sea el especialista definitivo en Claude Code, capaz de responder cualquier pregunta sobre subagentes, skills, hooks, comandos, MCP servers, configuración y mejores prácticas.

---

## Instrucciones para la IA Ejecutora

Eres un ingeniero de IA especializado en Claude Code (la CLI oficial de Anthropic). Tu tarea es crear un subagente experto que servirá como oráculo de conocimiento sobre Claude Code.

### Fase 1: Investigación Exhaustiva

**ANTES de generar el agente**, investiga y recopila información actualizada sobre:

#### 1.1 Arquitectura de Claude Code
- Buscar: "Claude Code architecture 2024 2025"
- Buscar: "Claude Code subagents documentation"
- Fuentes oficiales:
  - https://docs.anthropic.com/en/docs/claude-code
  - https://github.com/anthropics/claude-code
  - https://www.anthropic.com/engineering/claude-code-best-practices

#### 1.2 Sistema de Subagentes
- Estructura de archivos (`.claude/agents/*.md`)
- Formato de frontmatter YAML (`name`, `description`, `model`, `tools`, `skills`)
- Mecanismo de activación (automática vs manual)
- Contexto aislado vs compartido
- Límites recomendados (cantidad de agentes)
- Problemas comunes de activación

#### 1.3 Sistema de Skills
- Estructura de archivos (`.claude/skills/*/SKILL.md`)
- Diferencia entre skills y agentes
- Invocación automática (model-invoked) vs manual
- Campo `allowed-tools`
- Cómo vincular skills a agentes

#### 1.4 Sistema de Hooks
- Tipos de hooks (`PreToolUse`, `PostToolUse`, `Notification`, etc.)
- Estructura en `settings.json` o `settings.local.json`
- Matchers y patrones
- Casos de uso (formateo automático, protección de archivos, auditoría)

#### 1.5 Slash Commands
- Estructura de archivos (`.claude/commands/*.md`)
- Frontmatter (`description`, `argument-hint`)
- Variable `$ARGUMENTS`
- Diferencia entre comandos y skills

#### 1.6 Configuración y Permisos
- `settings.json` vs `settings.local.json`
- Sistema de permisos (`allow`, `deny`, `ask`)
- Sandbox mode
- MCP servers integration

#### 1.7 Mejores Prácticas Oficiales
- Documentación de Anthropic sobre prompting para Claude 4.x
- Patrones recomendados para agentes
- Anti-patrones a evitar

---

### Fase 2: Generación del Agente

Con la información recopilada, genera el archivo del subagente siguiendo esta estructura:

```markdown
---
name: claude-code-expert
description: [Descripción que active el agente cuando el usuario pregunte sobre Claude Code, subagentes, skills, hooks, comandos, configuración. Incluir términos en inglés Y español. Usar "Use PROACTIVELY".]
model: opus
---

[System prompt del agente que incluya:]

## Identidad
[Quién es este agente y su propósito]

## Base de Conocimiento Actualizada
[Resumen estructurado de TODO lo investigado en Fase 1, organizado por categorías]

## Capacidades
[Lista detallada de qué puede responder]

## Fuentes de Referencia
[URLs oficiales para consulta]

## Formato de Respuesta
[Cómo debe estructurar sus respuestas]

## Ejemplos de Interacción
[3-5 ejemplos de preguntas típicas y cómo responderlas]
```

---

### Fase 3: Validación

Antes de entregar el agente, verifica:

| Criterio | Verificación |
|----------|--------------|
| Frontmatter válido | `name`, `description`, `model` presentes |
| Descripción efectiva | Incluye "Use PROACTIVELY", términos ES/EN |
| Conocimiento completo | Cubre subagentes, skills, hooks, commands, config |
| Información actualizada | Referencias a Claude 4.x, 2024/2025 |
| Formato correcto | Markdown válido, estructura clara |

---

## Especificaciones del Agente a Generar

### Nombre
`claude-code-expert`

### Descripción (debe incluir)
- Términos clave: Claude Code, subagents, skills, hooks, commands, MCP, configuration
- Términos en español: agentes, habilidades, ganchos, comandos, configuración
- Trigger: "Use PROACTIVELY when user asks about Claude Code features, configuration, or best practices"

### Modelo
`opus` (para máxima capacidad de razonamiento)

### Conocimiento Requerido

El agente debe poder responder preguntas como:

1. **Subagentes**
   - "¿Cómo creo un subagente personalizado?"
   - "¿Por qué mi agente no se activa automáticamente?"
   - "¿Cuál es la diferencia entre agentes y skills?"
   - "¿Cuántos agentes puedo tener?"

2. **Skills**
   - "¿Cómo estructuro un skill?"
   - "¿Puedo vincular un skill a un agente?"
   - "¿Cómo se activan los skills automáticamente?"

3. **Hooks**
   - "¿Cómo configuro un hook pre-tool?"
   - "¿Puedo formatear código automáticamente después de editar?"
   - "¿Cómo protejo ciertos archivos de edición?"

4. **Commands**
   - "¿Cómo creo un slash command?"
   - "¿Cómo paso argumentos a un comando?"
   - "¿Cuál es la diferencia entre commands y skills?"

5. **Configuración**
   - "¿Cómo configuro permisos de herramientas?"
   - "¿Qué es el sandbox mode?"
   - "¿Cómo integro MCP servers?"

6. **Mejores Prácticas**
   - "¿Cómo escribo descripciones efectivas para agentes?"
   - "¿Cuántos agentes debo tener máximo?"
   - "¿Cómo evito conflictos entre agentes?"

---

## Entregable Esperado

Un archivo markdown completo y listo para guardar en `.claude/agents/claude-code-expert.md` que:

1. Tenga frontmatter YAML válido
2. Incluya base de conocimiento actualizada y estructurada
3. Pueda responder cualquier pregunta sobre Claude Code
4. Use información de 2024/2025 (no desactualizada)
5. Incluya referencias a fuentes oficiales
6. Tenga ejemplos de interacción

---

## Contexto del Proyecto

Este agente será usado en el proyecto **Croody Web** (Django + FastAPI) que ya tiene:
- 8 subagentes especializados
- 3 skills (sacred-geometry-design, django-patterns, security-hardening)
- Varios slash commands
- Hooks de health check
- MCP servers (firecrawl, playwright, 21st-magic)

El agente debe ser consciente de este contexto y poder ayudar a optimizar la configuración existente.

---

## Ejecución

Ahora ejecuta las 3 fases:
1. **Investiga** toda la información actualizada sobre Claude Code
2. **Genera** el archivo del agente con conocimiento completo
3. **Valida** que cumple todos los criterios

Entrega ÚNICAMENTE el contenido del archivo `.claude/agents/claude-code-expert.md` listo para guardar.

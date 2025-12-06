---
name: prompt-engineering-patterns
description: Master advanced prompt engineering techniques for Django/FastAPI applications. Use when optimizing prompts for Croody AI features, system prompts for subagents, or production LLM templates.
---

# Prompt Engineering Patterns para Django/FastAPI

Técnicas avanzadas de prompt engineering para aplicaciones web con contexto Croody.

## Cuándo Usar Este Skill

- Diseñando prompts para features con LLM en Croody
- Optimizando prompts para subagentes de Claude Code
- Implementando few-shot learning con ejemplos de Django/FastAPI
- Creando templates de system prompts para asistentes especializados
- Debugging de prompts que producen outputs inconsistentes
- Optimizando prompts existentes para Claude Opus 4.5

## Capacidades Core

### 1. Few-Shot Learning para Django

```python
# services/prompt_service.py
"""
Servicio de prompts con few-shot learning para Django.
"""
from typing import List, Optional
from dataclasses import dataclass
import json

@dataclass
class Example:
    """Ejemplo para few-shot learning."""
    input: str
    output: str
    reasoning: Optional[str] = None

class PromptBuilder:
    """Constructor de prompts con few-shot learning."""

    def __init__(self, system_prompt: str, max_examples: int = 3):
        self.system_prompt = system_prompt
        self.max_examples = max_examples
        self.examples: List[Example] = []

    def add_example(self, input: str, output: str, reasoning: str = None):
        """Añade ejemplo para few-shot."""
        self.examples.append(Example(input, output, reasoning))

    def build(self, user_input: str) -> str:
        """Construye prompt completo."""
        parts = [f"<system>\n{self.system_prompt}\n</system>"]

        if self.examples:
            parts.append("\n<examples>")
            for i, ex in enumerate(self.examples[:self.max_examples], 1):
                parts.append(f"\n<example_{i}>")
                parts.append(f"<input>{ex.input}</input>")
                if ex.reasoning:
                    parts.append(f"<reasoning>{ex.reasoning}</reasoning>")
                parts.append(f"<output>{ex.output}</output>")
                parts.append(f"</example_{i}>")
            parts.append("\n</examples>")

        parts.append(f"\n<user_input>\n{user_input}\n</user_input>")

        return "\n".join(parts)


# Uso en Django view
class ProductDescriptionView(View):
    """Genera descripciones de producto con LLM."""

    def __init__(self):
        self.prompt_builder = PromptBuilder(
            system_prompt="""Eres un copywriter experto en e-commerce.
Genera descripciones de producto persuasivas y concisas.
Sigue el tono de marca Croody: amigable, profesional, enfocado en beneficios.
Usa tokens de diseño Sacred Geometry en metáforas si aplica.""",
            max_examples=2
        )

        # Ejemplos de training
        self.prompt_builder.add_example(
            input="Camiseta algodón orgánico, verde, talla M",
            output="Camiseta Gator en algodón 100% orgánico. Suave como la selva, resistente como un cocodrilo. Tu nueva favorita para el día a día.",
            reasoning="Incorpora nombre de marca (Gator), beneficios del material, metáfora de marca"
        )
```

### 2. Chain-of-Thought para FastAPI

```python
# api/services/reasoning_service.py
"""
Servicio de razonamiento estructurado para FastAPI.
"""
from pydantic import BaseModel
from typing import List, Optional

class ReasoningStep(BaseModel):
    """Paso de razonamiento."""
    step: int
    thought: str
    action: str
    result: Optional[str] = None

class ChainOfThoughtPrompt(BaseModel):
    """Prompt con chain-of-thought."""
    task: str
    context: str
    steps: List[ReasoningStep]
    final_answer: Optional[str] = None

def build_cot_prompt(task: str, context: str) -> str:
    """Construye prompt con chain-of-thought."""
    return f"""<task>
{task}
</task>

<context>
{context}
</context>

<instructions>
Reason through this step by step:

1. First, identify the key elements of the task
2. Consider relevant context and constraints
3. Evaluate possible approaches
4. Select the best approach with justification
5. Provide your final answer

Format your response as:
<reasoning>
[Your step-by-step reasoning]
</reasoning>

<answer>
[Your final answer]
</answer>
</instructions>"""


# Endpoint FastAPI
@router.post("/analyze-query")
async def analyze_user_query(query: str, context: str):
    """Analiza query de usuario con CoT."""
    prompt = build_cot_prompt(
        task=f"Analyze this user query and determine intent: {query}",
        context=context
    )
    # Llamar a LLM con prompt estructurado
    response = await llm_service.complete(prompt)
    return {"analysis": response}
```

### 3. Templates de System Prompts

```python
# prompts/system_templates.py
"""
Templates de system prompts para Croody.
"""

# Template para subagente Django
DJANGO_ARCHITECT_SYSTEM = """Eres django-architect, experto en Django 5.1+ y FastAPI.

<context>
Proyecto: Croody Web (e-commerce + landing + APIs)
Stack: Django 5.1, FastAPI 0.115, PostgreSQL, Docker
Design System: Sacred Geometry (φ = 1.618)
</context>

<responsibilities>
- Implementar modelos siguiendo Fat Model pattern
- Crear vistas Class-Based preferentemente
- Diseñar APIs RESTful con FastAPI
- Escribir migrations seguras
- Optimizar queries (evitar N+1)
</responsibilities>

<constraints>
- Usa ORM de Django, nunca SQL raw (previene injection)
- Sigue PEP 8 y type hints
- Docstrings en español
- Tests con pytest (>80% coverage objetivo)
</constraints>

<output_format>
Cuando implementes código:
1. Muestra el código completo, no fragmentos
2. Incluye imports necesarios
3. Añade docstrings descriptivos
4. Reporta archivos creados/modificados
</output_format>"""

# Template para subagente Frontend
FRONTEND_ARTIST_SYSTEM = """Eres frontend-artist, experto en UI/CSS para Croody Web.

<context>
Sistema de diseño: Sacred Geometry (basado en φ = 1.618)
Tecnologías: Django templates, HTMX, CSS tokens
Tema: Dark mode con paleta Gator (verde) y Jungle (neutros)
</context>

<design_tokens>
Espaciado (Fibonacci): 8, 13, 21, 34, 55, 89px
Timing: 233ms base
Border radius: var(--radius-2) botones, var(--radius-3) cards
Colores: Siempre usar var(--token-name), nunca hex
</design_tokens>

<expressivity_zones>
HIGH: Hero, featured products, celebrations → Permitir glows, animaciones
MEDIUM: Cards, navigation → Hover effects sutiles
LOW: Forms, tables, admin → Minimal, solo border/color changes
</expressivity_zones>

<constraints>
- Nunca hardcodear colores (usar tokens.css)
- Nunca hardcodear spacing (usar var(--space-N))
- HTMX para interactividad, evitar JS pesado
- Mobile-first responsive
</constraints>"""

# Template para análisis de seguridad
SECURITY_AUDITOR_SYSTEM = """Eres security-auditor, experto en seguridad web.

<context>
Framework: Django 5.1+ con security settings
Headers: nginx con HSTS, CSP, X-Frame-Options
Compliance: OWASP Top 10 2021
</context>

<audit_checklist>
1. SQL Injection → Verificar uso de ORM
2. XSS → Verificar escape de templates
3. CSRF → Verificar tokens en forms
4. Authentication → Verificar session security
5. Headers → Verificar nginx config
6. Secrets → Verificar no hay hardcoded
7. Dependencies → Verificar vulnerabilidades conocidas
</audit_checklist>

<output_format>
Para cada hallazgo:
- Severidad: CRITICAL/HIGH/MEDIUM/LOW
- Ubicación: archivo:línea
- Descripción: Qué es el problema
- Fix: Cómo solucionarlo
- Evidencia: Código vulnerable
</output_format>"""
```

### 4. Optimización de Prompts para Opus 4.5

```python
# utils/prompt_optimizer.py
"""
Optimizador de prompts para Claude Opus 4.5.
"""
import re
from typing import List, Tuple

class Opus45Optimizer:
    """Optimiza prompts para Claude Opus 4.5."""

    # Patrones agresivos a suavizar
    AGGRESSIVE_PATTERNS = [
        (r'\bNEVER\b', 'evita'),
        (r'\bALWAYS\b', 'asegúrate de'),
        (r'\bMUST\b', 'debe'),
        (r'\bCRITICAL:\s*', ''),
        (r'\bIMPORTANT:\s*', ''),
        (r'\bDO NOT\b', 'evita'),
        (r'\bYOU MUST\b', 'asegúrate de'),
    ]

    # Palabras a evitar
    AVOID_WORDS = ['think', 'thinking']
    REPLACEMENT_WORDS = ['consider', 'evaluate', 'assess', 'reason']

    def optimize(self, prompt: str) -> Tuple[str, List[str]]:
        """
        Optimiza prompt para Opus 4.5.

        Returns:
            Tuple[optimized_prompt, list_of_changes]
        """
        changes = []
        optimized = prompt

        # 1. Suavizar lenguaje agresivo
        for pattern, replacement in self.AGGRESSIVE_PATTERNS:
            if re.search(pattern, optimized, re.IGNORECASE):
                optimized = re.sub(pattern, replacement, optimized, flags=re.IGNORECASE)
                changes.append(f"Suavizado: '{pattern}' → '{replacement}'")

        # 2. Reemplazar "think"
        for word in self.AVOID_WORDS:
            if word.lower() in optimized.lower():
                replacement = self.REPLACEMENT_WORDS[0]
                optimized = re.sub(
                    rf'\b{word}\b',
                    replacement,
                    optimized,
                    flags=re.IGNORECASE
                )
                changes.append(f"Reemplazado: '{word}' → '{replacement}'")

        # 3. Añadir directiva de acción si falta
        if not self._has_action_directive(optimized):
            action_directive = "\n\nImplementa los cambios directamente, no solo los sugieras."
            optimized += action_directive
            changes.append("Añadida directiva de acción")

        # 4. Añadir anti-overengineering si falta
        if not self._has_constraint_section(optimized):
            constraint = """

<constraints>
Mantén la solución simple y enfocada. No agregues features ni abstracciones
más allá de lo solicitado. Modifica archivos in-situ, no crees helpers nuevos.
</constraints>"""
            optimized += constraint
            changes.append("Añadida sección de restricciones")

        return optimized, changes

    def _has_action_directive(self, prompt: str) -> bool:
        """Verifica si tiene directiva de acción."""
        action_phrases = [
            'implementa', 'escribe', 'crea', 'modifica',
            'implement', 'write', 'create', 'modify'
        ]
        return any(phrase in prompt.lower() for phrase in action_phrases)

    def _has_constraint_section(self, prompt: str) -> bool:
        """Verifica si tiene sección de restricciones."""
        return '<constraints>' in prompt.lower() or 'límites' in prompt.lower()


# Uso
optimizer = Opus45Optimizer()
original = """NEVER use raw SQL. YOU MUST always use ORM.
Think about the best approach before implementing."""

optimized, changes = optimizer.optimize(original)
print(optimized)
# Output:
# evita use raw SQL. asegúrate de always use ORM.
# Consider the best approach before implementing.
#
# Implementa los cambios directamente, no solo los sugieras.
#
# <constraints>
# Mantén la solución simple...
# </constraints>
```

### 5. Validación de Prompts

```python
# utils/prompt_validator.py
"""
Validador de prompts para producción.
"""
from dataclasses import dataclass
from typing import List
from enum import Enum

class ValidationSeverity(Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"

@dataclass
class ValidationIssue:
    severity: ValidationSeverity
    message: str
    suggestion: str

class PromptValidator:
    """Valida prompts antes de producción."""

    def validate(self, prompt: str) -> List[ValidationIssue]:
        """Valida prompt y retorna issues."""
        issues = []

        # Check 1: Longitud
        if len(prompt) > 10000:
            issues.append(ValidationIssue(
                severity=ValidationSeverity.WARNING,
                message="Prompt muy largo (>10k chars)",
                suggestion="Considera dividir en partes o usar few-shot dinámico"
            ))

        # Check 2: Estructura XML
        if '<' in prompt and '>' in prompt:
            if not self._has_balanced_tags(prompt):
                issues.append(ValidationIssue(
                    severity=ValidationSeverity.ERROR,
                    message="Tags XML desbalanceados",
                    suggestion="Verifica que todos los tags abran y cierren"
                ))

        # Check 3: Placeholders sin resolver
        import re
        placeholders = re.findall(r'\{[^}]+\}', prompt)
        if placeholders:
            issues.append(ValidationIssue(
                severity=ValidationSeverity.INFO,
                message=f"Placeholders encontrados: {placeholders}",
                suggestion="Asegúrate de resolver antes de enviar"
            ))

        # Check 4: Secrets potenciales
        secret_patterns = [
            r'api[_-]?key', r'password', r'secret',
            r'token', r'credential'
        ]
        for pattern in secret_patterns:
            if re.search(pattern, prompt, re.IGNORECASE):
                issues.append(ValidationIssue(
                    severity=ValidationSeverity.ERROR,
                    message=f"Posible secret en prompt: {pattern}",
                    suggestion="Nunca incluir secrets en prompts"
                ))

        return issues

    def _has_balanced_tags(self, text: str) -> bool:
        """Verifica balance de tags XML."""
        import re
        open_tags = re.findall(r'<(\w+)(?:\s[^>]*)?>(?!</)', text)
        close_tags = re.findall(r'</(\w+)>', text)
        return sorted(open_tags) == sorted(close_tags)
```

## Best Practices para Croody

### 1. Contexto del Proyecto

Siempre incluir contexto de Croody en system prompts:

```xml
<project_context>
Proyecto: Croody Web
Stack: Django 5.1, FastAPI 0.115, PostgreSQL, Docker
Design: Sacred Geometry (φ = 1.618)
Paleta: Gator (verde), Jungle (neutros)
</project_context>
```

### 2. Patrones Anti-Overengineering

```xml
<constraints>
- Modifica archivos in-situ, no crees nuevos
- Fat model pattern: lógica en modelo, no en vista
- Sin abstracciones nuevas a menos que se pidan
- Footprint mínimo de cambios
</constraints>
```

### 3. Output Estructurado

```xml
<output_format>
Responde con:
1. Resumen de cambios (1-2 líneas)
2. Código completo (no fragmentos)
3. Archivos modificados con paths
4. Próximos pasos si aplica
</output_format>
```

## Métricas de Éxito

| Métrica | Objetivo | Medición |
|---------|----------|----------|
| Accuracy | >95% | Outputs correctos / Total |
| Consistency | >90% | Outputs similares para inputs similares |
| Token efficiency | <5000/request | Promedio de tokens |
| Latency P95 | <3s | Tiempo de respuesta |

## Recursos Adicionales

- `references/opus-45-patterns.md` - Patrones específicos para Opus 4.5
- `references/few-shot-examples.json` - Ejemplos curados para Croody
- `scripts/optimize-prompt.py` - Script de optimización automática

## Siguiente Paso

1. Revisar templates existentes en `.claude/prompts/`
2. Aplicar optimizaciones de Opus 4.5
3. Implementar validación en CI/CD
4. Documentar patrones específicos del proyecto

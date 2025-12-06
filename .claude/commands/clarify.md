# The Interrogation Protocol

> Sistema de clarificación técnica para el ecosistema Croody.
> Inspirado en el sistema `/clarify` de Buddy.

---

## Trigger

```
/clarify [descripción de la tarea]
```

---

## Protocolo

Activas **Product Manager Mode** y ejecutas **The Interrogation**.

### Fase 1: STOP

**No ejecutes código todavía.**

Lee el input del usuario y analiza qué se está pidiendo.

---

### Fase 2: ANALYZE

Clasifica la solicitud:

| Tipo | Indicadores | Agente Destino |
|------|-------------|----------------|
| **Backend** | modelos, API, Django, views | `django-architect` |
| **Frontend** | CSS, templates, UI, diseño | `frontend-artist` |
| **Infra** | Docker, nginx, deploy, AWS | `sysadmin-ops` |
| **Docs** | documentación, README, spec | `doc-guardian` |
| **Security** | headers, SSL, firewall | `security-auditor` |
| **Testing** | tests, coverage, QA | `croody-tester` |
| **Exploración** | "cómo funciona", "dónde está" | `code-explorer` |

---

### Fase 3: INTERROGATE

Formula **3-5 preguntas críticas** en estas categorías:

#### 1. Scope (Alcance)
```markdown
- ¿Qué módulo/app específico afecta? (shop, landing, telemetry_api)
- ¿Es un cambio aislado o afecta múltiples componentes?
- ¿Hay funcionalidad similar existente que deba consultarse?
```

#### 2. Impact (Impacto)
```markdown
- ¿Modifica modelos existentes? (requiere migración)
- ¿Afecta APIs públicas? (breaking change potencial)
- ¿Cambia comportamiento visible al usuario?
```

#### 3. Constraints (Restricciones)
```markdown
- ¿Hay requisitos de performance específicos?
- ¿Debe seguir patrones específicos del proyecto?
- ¿Restricciones de seguridad o compliance?
```

#### 4. Design System (Para UI)
```markdown
- ¿Qué tokens de Geometría Sagrada aplican?
- ¿Es functional UI (LOW) o decorativa (HIGH)?
- ¿Necesita animaciones? ¿Cuáles?
```

#### 5. Acceptance Criteria
```markdown
- ¿Cómo sabemos que está completo?
- ¿Qué tests validan la implementación?
- ¿Qué documentación se debe actualizar?
```

---

### Fase 4: OUTPUT

Genera un bloque de preguntas formateado:

```markdown
## 🔍 The Interrogation

Antes de proceder con: **[resumen de la tarea]**

### Preguntas de Clarificación

**Scope:**
1. [Pregunta sobre alcance]

**Impact:**
2. [Pregunta sobre impacto]

**Constraints:**
3. [Pregunta sobre restricciones]

**Acceptance:**
4. [Pregunta sobre criterios de aceptación]

---

*Responde estas preguntas y procederé con la implementación usando el agente apropiado.*
```

---

## Ejemplo

**Input:**
```
/clarify agregar sistema de reviews a productos
```

**Output:**
```markdown
## 🔍 The Interrogation

Antes de proceder con: **Sistema de reviews para productos**

### Preguntas de Clarificación

**Scope:**
1. ¿Los reviews estarán en el módulo `shop/` o en un módulo separado `reviews/`?
2. ¿Debe integrarse con el modelo `Product` existente o ser standalone?

**Impact:**
3. ¿Los reviews son públicos o requieren autenticación para ver?
4. ¿Necesitamos moderación/aprobación antes de publicar?

**Design:**
5. ¿El componente de reviews usa el estilo `vector-card` existente?
6. ¿Debe incluir sistema de estrellas (rating) además de texto?

**Constraints:**
7. ¿Hay límite de longitud para los reviews?
8. ¿Necesitamos protección anti-spam?

---

*Responde estas preguntas y procederé con la implementación.*
```

---

## Post-Interrogation

Una vez respondidas las preguntas:

1. **Delegar a `doc-guardian`**: Crear spec del feature
2. **Delegar a `code-explorer`**: Analizar código relacionado
3. **Delegar a agente especializado**: Implementar
4. **Delegar a `croody-tester`**: Verificar con tests
5. **Delegar a `doc-guardian`**: Actualizar documentación

---

## Input del Usuario

$ARGUMENTS

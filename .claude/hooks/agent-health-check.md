# Agent Health Check Protocol

## Propósito

Protocolo para verificar que los subagentes completen sus tareas correctamente antes de reportar al usuario.

## Checklist Post-Task

Después de recibir respuesta de un subagente, el orquestador debe verificar:

### 1. Completitud de Respuesta

- [ ] El agente reportó archivos creados/modificados
- [ ] El agente incluyó resumen de cambios
- [ ] El agente sugirió próximos pasos (si aplica)
- [ ] El agente verificó quality gates (si aplica)

### 2. Formato de Respuesta Esperado

El agente debe haber respondido con estructura:

```markdown
## Completado / ## Code Review / ## Análisis / etc.

**Archivos creados:**
- [path/to/file.py]

**Archivos modificados:**
- [path/to/existing.py]

**Resumen:**
[Descripción de lo que se hizo]

**Quality Gates:**
- [ ] Tests pasan
- [ ] Linting OK
- [ ] Docs actualizados

**Próximos pasos:**
1. [sugerencia]
```

### 3. Indicadores de Fallo

Si la respuesta contiene:
- "No pude completar..."
- "Error al..."
- "Falta información..."
- "No encontré el archivo..."
- Sin sección de archivos/resumen

→ Re-invocar con más contexto o reportar al usuario

### 4. Acciones por Estado

| Estado | Acción |
|--------|--------|
| Completo con estructura | Consolidar y reportar al usuario |
| Completo sin estructura | Solicitar clarificación al agente |
| Parcialmente completo | Re-invocar con contexto adicional |
| Fallido | Reportar al usuario, sugerir alternativas |
| Bloqueado | Identificar bloqueador, escalar si es necesario |

### 5. Validación por Tipo de Agente

#### django-architect

```markdown
## Verificar
- [ ] Migrations creadas (si modificó modelos)
- [ ] Docstrings en Python
- [ ] Imports ordenados
- [ ] No raw SQL sin parametrizar
- [ ] Fat model pattern seguido
```

#### frontend-artist

```markdown
## Verificar
- [ ] Tokens CSS usados (no hardcoded)
- [ ] BEM naming convention
- [ ] No inline styles
- [ ] Accesibilidad básica
```

#### sysadmin-ops

```markdown
## Verificar
- [ ] No comandos sudo sin explicación
- [ ] Scripts con comentarios
- [ ] Rollback plan incluido
- [ ] No secrets expuestos
```

#### security-auditor

```markdown
## Verificar
- [ ] OWASP reference incluida
- [ ] Severity clasificada
- [ ] Remediation steps claros
- [ ] Compliance status actualizado
```

#### croody-tester

```markdown
## Verificar
- [ ] Tests ejecutables
- [ ] Fixtures incluidas
- [ ] Coverage reportado
- [ ] Edge cases cubiertos
```

## Integración con Quality Gates

Este protocolo complementa los Quality Gates existentes en CLAUDE.md:

1. **Completitud** → Health Check verifica estructura de respuesta
2. **Consistencia** → Orquestador valida contra patrones del proyecto
3. **Documentación** → Orquestador verifica si docs necesitan actualización
4. **Testing** → Orquestador verifica si tests fueron sugeridos/creados

## Ejemplo de Verificación

```markdown
[Respuesta del subagente recibida]

Health Check:
✓ Archivos reportados: 2 creados, 1 modificado
✓ Resumen presente: "Implementado modelo Review con campos rating, comment, is_approved"
✓ Próximos pasos: "Crear vistas, agregar tests"
✓ Migration incluida
✗ Tests no creados (esperado para siguiente fase)
→ PASS - Proceder a consolidar

Consolidación para usuario:
"Se creó el modelo Review en shop/models.py con los campos solicitados.
Próximo paso recomendado: crear las vistas y tests."
```

## Ejemplo de Fallo

```markdown
[Respuesta del subagente recibida]

Health Check:
✓ Archivos reportados: 1 modificado
✗ Resumen genérico: "Cambios realizados"
✗ Sin próximos pasos
✗ Sin verification de quality gates
→ FAIL - Solicitar clarificación

Acción:
Re-invocar agente con prompt: "Por favor proporciona:
1. Resumen detallado de los cambios
2. Verificación de que sigue fat model pattern
3. Próximos pasos sugeridos"
```

## Post-Task Actions

Después de verificación exitosa:

1. **Consolidar** resultados de múltiples agentes
2. **Formatear** respuesta para el usuario
3. **Sugerir** siguiente paso lógico
4. **Actualizar** documentación si es necesario

## Error Recovery

Si un agente falla repetidamente:

1. **Cambiar estrategia**: Usar agente diferente o combinar
2. **Escalar**: Reportar al usuario con opciones
3. **Documentar**: Registrar el problema para mejora

```markdown
"El agente django-architect tuvo problemas con [X].
Opciones:
1. Intentar con más contexto
2. Dividir la tarea en partes más pequeñas
3. Proceder manualmente con mi guía
¿Qué prefieres?"
```

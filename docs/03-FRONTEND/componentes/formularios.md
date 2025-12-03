# Componente Formulario - Documentación Completa

## Resumen
El sistema de formularios de Croody implementa un diseño consistente y accesible basado en **tokens CSS** y principios de **usabilidad**. Soporta inputs, textareas, selects, checkboxes, radio buttons con validaciones visuales, estados interactivos y layouts responsivos.

## Ubicación
- **CSS Base**: `/proyecto_integrado/Croody/static/css/base.css` (líneas 47-187)
- **Componentes**: `/proyecto_integrado/Croody/static/css/components.css` (líneas 76-182, 117-120, 170-181)
- **Tokens**: `/proyecto_integrado/Croody/static/css/tokens.css`

## Anatomía del Formulario

### Estructura Base
```
┌─────────────────────────────────────────┐
│ Form Container                           │
│ ┌─────────────────────────────────────┐ │
│ │ Field Group                         │ │
│ │ ┌─────────────────────────────────┐ │ │
│ │ │ Label                           │ │ │
│ │ │ Input/Textarea/Select          │ │ │
│ │ │ Helper Text (Opcional)         │ │ │
│ │ │ Error Message (Si aplica)      │ │ │
│ │ └─────────────────────────────────┘ │ │
│ │ ┌─────────────────────────────────┐ │ │
│ │ │ Submit Actions                  │ │ │
│ │ │ [Cancel] [Submit]               │ │ │
│ │ └─────────────────────────────────┘ │ │
│ └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

## Componentes de Formulario

### 1. Input Field

**Base Styles**:
```css
input[type="text"],
input[type="email"],
input[type="password"],
input[type="search"],
input[type="url"],
input[type="tel"],
input[type="number"],
input[type="date"],
textarea,
select {
  font-family: var(--font-sans);
  font-size: var(--text-base);
  line-height: var(--leading-base);
  background: var(--surface-2);
  border: 1px solid color-mix(in oklab, var(--brand-base), transparent 70%);
  border-radius: 12px;
  padding: var(--space-2);
  color: var(--fg);
  transition: border-color 233ms cubic-bezier(.2,.8,.2,1),
              box-shadow 233ms;
  width: 100%;
}
```

**Focus State**:
```css
input:focus-visible,
textarea:focus-visible,
select:focus-visible {
  outline: 2px solid var(--focus-ring);
  outline-offset: 3px;
  border-color: var(--brand-base);
  box-shadow: 0 0 0 var(--focus-ring-offset) color-mix(in oklab, var(--brand-base) 20%, transparent);
}
```

#### Ejemplo de Input
```html
<div class="field">
  <label for="email" class="field__label">Email</label>
  <input
    type="email"
    id="email"
    name="email"
    class="field__input"
    placeholder="tu@email.com"
    required
  >
  <p class="field__hint">Usaremos este email para enviar confirmaciones</p>
</div>
```

#### Field Variants
```css
/* Input Pequeño */
.field--sm .field__input {
  height: 40px;
  padding: 0 12px;
  font-size: var(--text-sm);
}

/* Input Grande */
.field--lg .field__input {
  height: 60px;
  padding: 0 24px;
  font-size: var(--text-lg);
}

/* Input con Icono */
.field--icon-left .field__input {
  padding-left: 48px;
}

.field--icon-left .field__icon {
  position: absolute;
  left: 16px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--fg-subtle);
  pointer-events: none;
}

/* Input con Estado */
.field__input.is-valid {
  border-color: var(--gator-500);
  background: color-mix(in oklab, var(--gator-500) 5%, var(--surface-2));
}

.field__input.is-invalid {
  border-color: var(--error-500);
  background: color-mix(in oklab, var(--error-500) 5%, var(--surface-2));
}
```

### 2. Textarea

**Características**:
- Redimensionable verticalmente (por defecto)
- Altura mínima automática
- Contador de caracteres opcional

```css
textarea {
  min-height: 120px;
  resize: vertical;
  font-family: var(--font-sans);
}

textarea[readonly] {
  resize: none;
  background: var(--surface-1);
}
```

**Ejemplo**:
```html
<div class="field">
  <label for="message" class="field__label">Mensaje</label>
  <textarea
    id="message"
    name="message"
    class="field__input"
    rows="4"
    maxlength="500"
    placeholder="Escribe tu mensaje aquí..."
    required
  ></textarea>
  <div class="field__meta">
    <p class="field__hint">Máximo 500 caracteres</p>
    <span class="field__counter">0/500</span>
  </div>
</div>
```

**CSS Adicional**:
```css
.field__meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: var(--space-1);
}

.field__counter {
  font-size: 0.85rem;
  color: var(--fg-subtle);
}

.field__counter.over-limit {
  color: var(--error-500);
  font-weight: 600;
}
```

### 3. Select (Dropdown)

**Estilos**:
```css
select {
  appearance: none;
  background-image: url("data:image/svg+xml;charset=UTF-8,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3e%3cpolyline points='6,9 12,15 18,9'%3e%3c/polyline%3e%3c/svg%3e");
  background-repeat: no-repeat;
  background-position: right 12px center;
  background-size: 16px;
  padding-right: 40px;
  cursor: pointer;
}

select:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  background-color: var(--surface-1);
}
```

**Ejemplo con Optgroups**:
```html
<div class="field">
  <label for="country" class="field__label">País</label>
  <select id="country" name="country" class="field__input" required>
    <option value="">Selecciona un país</option>
    <optgroup label="Europa">
      <option value="es">España</option>
      <option value="fr">Francia</option>
      <option value="de">Alemania</option>
    </optgroup>
    <optgroup label="América">
      <option value="us">Estados Unidos</option>
      <option value="mx">México</option>
    </optgroup>
  </select>
</div>
```

### 4. Checkbox

**Accent Color**:
```css
input[type="checkbox"] {
  accent-color: var(--brand-base);
  width: 20px;
  height: 20px;
  cursor: pointer;
}
```

**Ejemplo**:
```html
<div class="checkbox">
  <input
    type="checkbox"
    id="terms"
    name="terms"
    class="checkbox__input"
    required
  >
  <label for="terms" class="checkbox__label">
    Acepto los <a href="/terms">términos y condiciones</a>
  </label>
</div>
```

**CSS Custom**:
```css
.checkbox {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.checkbox__input {
  flex-shrink: 0;
  width: 20px;
  height: 20px;
  margin-top: 2px;
  cursor: pointer;
}

.checkbox__label {
  color: var(--fg);
  cursor: pointer;
  line-height: 1.5;
}

.checkbox__label a {
  color: var(--brand-base);
  text-decoration: underline;
}
```

### 5. Radio Button

**Ejemplo**:
```html
<div class="radio-group">
  <label class="radio-group__label">Tipo de cuenta</label>

  <div class="radio">
    <input
      type="radio"
      id="account-personal"
      name="account-type"
      value="personal"
      class="radio__input"
      checked
    >
    <label for="account-personal" class="radio__label">
      <span class="radio__custom"></span>
      Personal
    </label>
  </div>

  <div class="radio">
    <input
      type="radio"
      id="account-business"
      name="account-type"
      value="business"
      class="radio__input"
    >
    <label for="account-business" class="radio__label">
      <span class="radio__custom"></span>
      Empresarial
    </label>
  </div>
</div>
```

**CSS Custom**:
```css
.radio-group {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.radio-group__label {
  font-weight: 600;
  color: var(--fg);
  margin-bottom: var(--space-1);
}

.radio {
  display: flex;
  align-items: center;
  gap: 12px;
}

.radio__input {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
}

.radio__custom {
  width: 20px;
  height: 20px;
  border: 2px solid var(--border-2);
  border-radius: 50%;
  display: inline-block;
  position: relative;
  cursor: pointer;
  transition: border-color 233ms ease;
}

.radio__custom::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 10px;
  height: 10px;
  background: var(--brand-base);
  border-radius: 50%;
  transform: translate(-50%, -50%) scale(0);
  transition: transform 233ms cubic-bezier(.2,.8,.2,1);
}

.radio__input:checked + .radio__label .radio__custom {
  border-color: var(--brand-base);
}

.radio__input:checked + .radio__label .radio__custom::after {
  transform: translate(-50%, -50%) scale(1);
}

.radio__label {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  color: var(--fg);
}
```

### 6. Switch Toggle

**Ejemplo**:
```html
<div class="switch">
  <input
    type="checkbox"
    id="notifications"
    name="notifications"
    class="switch__input"
  >
  <label for="notifications" class="switch__label">
    <span class="switch__track"></span>
    <span class="switch__thumb"></span>
    <span class="switch__text">Notificaciones</span>
  </label>
</div>
```

**CSS**:
```css
.switch__input {
  position: absolute;
  opacity: 0;
  width: 0;
  height: 0;
}

.switch__label {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  user-select: none;
}

.switch__track {
  width: 48px;
  height: 28px;
  background: var(--surface-2);
  border: 1px solid var(--border-1);
  border-radius: 28px;
  position: relative;
  transition: background 233ms ease, border-color 233ms ease;
}

.switch__thumb {
  width: 22px;
  height: 22px;
  background: var(--fg-muted);
  border-radius: 50%;
  position: absolute;
  top: 2px;
  left: 2px;
  transition: left 233ms cubic-bezier(.2,.8,.2,1),
              background 233ms ease;
}

.switch__input:checked + .switch__label .switch__track {
  background: var(--brand-base);
  border-color: var(--brand-base);
}

.switch__input:checked + .switch__label .switch__thumb {
  left: 24px;
  background: white;
}

.switch__text {
  color: var(--fg);
  font-size: var(--text-base);
}
```

## Layouts de Formulario

### 1. Form Vertical (Default)

```html
<form class="form form--vertical">
  <div class="field">
    <label for="name" class="field__label">Nombre</label>
    <input type="text" id="name" class="field__input" required>
  </div>

  <div class="field">
    <label for="email" class="field__label">Email</label>
    <input type="email" id="email" class="field__input" required>
  </div>

  <div class="form__actions">
    <button type="submit" class="btn btn--primary">Enviar</button>
  </div>
</form>
```

**CSS**:
```css
.form {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.form--vertical .field {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.form__actions {
  display: flex;
  gap: var(--space-2);
  margin-top: var(--space-3);
}

.form__actions .btn {
  flex: 1;
}
```

### 2. Form Horizontal

```html
<form class="form form--horizontal">
  <div class="field field--inline">
    <label for="search" class="field__label">Buscar</label>
    <input type="search" id="search" class="field__input" placeholder="Término de búsqueda">
    <button type="submit" class="btn btn--primary">Buscar</button>
  </div>
</form>
```

**CSS**:
```css
.form--horizontal .field--inline {
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: center;
  gap: var(--space-2);
}

@media (max-width: 767.98px) {
  .form--horizontal .field--inline {
    grid-template-columns: 1fr;
  }
}
```

### 3. Form Multi-Column

```html
<form class="form form--grid">
  <div class="field">
    <label for="first-name" class="field__label">Nombre</label>
    <input type="text" id="first-name" class="field__input">
  </div>

  <div class="field">
    <label for="last-name" class="field__label">Apellido</label>
    <input type="text" id="last-name" class="field__input">
  </div>

  <div class="field field--full">
    <label for="address" class="field__label">Dirección</label>
    <input type="text" id="address" class="field__input">
  </div>
</form>
```

**CSS**:
```css
.form--grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--space-2);
}

.form--grid .field--full {
  grid-column: 1 / -1;
}

@media (max-width: 767.98px) {
  .form--grid {
    grid-template-columns: 1fr;
  }
}
```

### 4. Inline Form

```html
<form class="form form--inline">
  <input type="email" class="field__input" placeholder="Tu email">
  <button type="submit" class="btn btn--primary">Suscribirse</button>
</form>
```

**CSS**:
```css
.form--inline {
  display: flex;
  gap: var(--space-2);
  align-items: center;
}

.form--inline .field__input {
  flex: 1;
}

@media (max-width: 767.98px) {
  .form--inline {
    flex-direction: column;
    align-items: stretch;
  }
}
```

## Estados de Validación

### 1. Success State
```css
.field__input.is-valid {
  border-color: var(--gator-500);
  background: color-mix(in oklab, var(--gator-500) 5%, var(--surface-2));
}

.field__input.is-valid + .field__icon {
  color: var(--gator-500);
}
```

### 2. Error State
```css
.field__input.is-invalid {
  border-color: var(--error-500);
  background: color-mix(in oklab, var(--error-500) 5%, var(--surface-2));
}

.field__error {
  color: var(--error-500);
  font-size: 0.85rem;
  margin-top: 4px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.field__error::before {
  content: '⚠';
}
```

**Ejemplo**:
```html
<div class="field">
  <label for="password" class="field__label">Contraseña</label>
  <input
    type="password"
    id="password"
    class="field__input is-invalid"
    value="123"
  >
  <p class="field__error">La contraseña debe tener al menos 8 caracteres</p>
</div>
```

### 3. Loading State
```css
.field__input.is-loading {
  position: relative;
}

.field__input.is-loading::after {
  content: '';
  position: absolute;
  right: 12px;
  top: 50%;
  width: 16px;
  height: 16px;
  margin: -8px;
  border: 2px solid var(--fg-muted);
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}
```

## Formularios Específicos

### 1. Search Form

**Ubicación**: Header, catálogo de productos

```html
<form class="search" role="search">
  <label for="search-input" class="visually-hidden">Buscar</label>
  <input
    type="search"
    id="search-input"
    name="q"
    class="search__input"
    placeholder="Buscar productos..."
    autocomplete="off"
  >
  <span class="search__icon">🔍</span>
</form>
```

**CSS**:
```css
.search {
  position: relative;
}

.search__input {
  height: 44px;
  padding: 0 38px 0 16px;
  border-radius: var(--radius-3);
  border: 1.5px solid color-mix(in oklab, var(--brand-base), var(--fg) 30%);
  background: color-mix(in oklab, var(--surface-1), transparent 5%);
  color: var(--fg);
  transition: border-color 233ms cubic-bezier(.2,.8,.2,1),
              box-shadow 233ms;
}

.search__input:focus-visible {
  outline: 2px solid var(--focus-ring);
  outline-offset: 3px;
  box-shadow: 0 8px 21px color-mix(in oklab, var(--focus-ring), transparent 78%);
}

.search__icon {
  position: absolute;
  right: 13px;
  top: 50%;
  translate: 0 -50%;
  font-size: 0.8rem;
  color: var(--fg-tertiary);
}
```

### 2. Authentication Form

```html
<form class="auth-form" method="post">
  {% csrf_token %}

  <div class="field">
    <label for="id_username" class="field__label">
      {{ form.username.label }}
    </label>
    {{ form.username }}
    {% if form.username.errors %}
      <p class="field__error">{{ form.username.errors|join:", " }}</p>
    {% endif %}
  </div>

  <div class="field">
    <label for="id_password" class="field__label">
      {{ form.password.label }}
    </label>
    {{ form.password }}
    {% if form.password.errors %}
      <p class="field__error">{{ form.password.errors|join:", " }}</p>
    {% endif %}
  </div>

  <div class="checkbox">
    {{ form.remember_me }}
    <label for="id_remember_me" class="checkbox__label">
      Recordarme
    </label>
  </div>

  <button type="submit" class="btn btn--primary btn--full">
    Acceder
  </button>

  <p class="auth-alt">
    <a href="{% url 'landing:signup' %}">¿No tienes cuenta? Regístrate</a>
  </p>
</form>
```

**CSS**:
```css
.auth-form {
  padding: var(--space-4);
  background: var(--surface-1);
  border-radius: 24px;
  border: 1px solid color-mix(in oklab, var(--brand-base), transparent 70%);
  box-shadow: var(--shadow);
}

.btn--full {
  width: 100%;
}

.auth-alt {
  margin-top: var(--space-2);
  font-size: 0.9rem;
  text-align: center;
}

.auth-alt a {
  color: var(--brand-base);
  text-decoration: underline;
}
```

### 3. Profile Form

```html
<form class="profile-form" method="post">
  {% csrf_token %}

  <fieldset class="form-section">
    <legend>Información Personal</legend>

    <div class="field">
      <label for="id_full_name" class="field__label">Nombre Completo</label>
      {{ form.full_name }}
    </div>

    <div class="field">
      <label for="id_email" class="field__label">Email</label>
      {{ form.email }}
    </div>

    <div class="field">
      <label for="id_phone" class="field__label">Teléfono</label>
      {{ form.phone }}
    </div>
  </fieldset>

  <fieldset class="form-section">
    <legend>Preferencias</legend>

    <div class="field">
      <label for="id_preferred_language" class="field__label">Idioma</label>
      {{ form.preferred_language }}
    </div>

    <div class="field">
      <label for="id_preferred_theme" class="field__label">Tema</label>
      {{ form.preferred_theme }}
    </div>

    <div class="switch">
      {{ form.email_notifications }}
      <label for="id_email_notifications" class="switch__label">
        <span class="switch__track"></span>
        <span class="switch__thumb"></span>
        <span class="switch__text">Notificaciones por email</span>
      </label>
    </div>
  </fieldset>

  <div class="form__actions">
    <button type="submit" class="btn btn--primary">Guardar Cambios</button>
  </div>
</form>
```

**CSS**:
```css
.form-section {
  padding: var(--space-3);
  border: 1px solid var(--border-1);
  border-radius: 16px;
  margin-bottom: var(--space-2);
}

.form-section legend {
  padding: 0 var(--space-2);
  font-weight: 600;
  color: var(--fg);
}

.form-section .field {
  margin-bottom: var(--space-2);
}
```

## Validación con JavaScript

### Real-time Validation
```javascript
function initFormValidation() {
  const forms = document.querySelectorAll('form[data-validate]');

  forms.forEach(form => {
    const fields = form.querySelectorAll('.field__input');

    fields.forEach(field => {
      field.addEventListener('blur', () => validateField(field));
      field.addEventListener('input', () => clearValidation(field));
    });

    form.addEventListener('submit', (e) => {
      if (!validateForm(form)) {
        e.preventDefault();
      }
    });
  });
}

function validateField(field) {
  const value = field.value.trim();
  const type = field.type;
  let isValid = true;
  let errorMessage = '';

  // Required validation
  if (field.required && !value) {
    isValid = false;
    errorMessage = 'Este campo es obligatorio';
  }

  // Email validation
  else if (type === 'email' && value) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(value)) {
      isValid = false;
      errorMessage = 'Introduce un email válido';
    }
  }

  // Password validation
  else if (type === 'password' && value) {
    if (value.length < 8) {
      isValid = false;
      errorMessage = 'La contraseña debe tener al menos 8 caracteres';
    }
  }

  // Apply validation state
  if (isValid) {
    field.classList.remove('is-invalid');
    field.classList.add('is-valid');
    removeErrorMessage(field);
  } else {
    field.classList.remove('is-valid');
    field.classList.add('is-invalid');
    showErrorMessage(field, errorMessage);
  }

  return isValid;
}

function showErrorMessage(field, message) {
  removeErrorMessage(field);

  const errorElement = document.createElement('p');
  errorElement.className = 'field__error';
  errorElement.textContent = message;

  field.parentNode.appendChild(errorElement);
}

function removeErrorMessage(field) {
  const errorElement = field.parentNode.querySelector('.field__error');
  if (errorElement) {
    errorElement.remove();
  }
}

function validateForm(form) {
  const fields = form.querySelectorAll('.field__input');
  let isFormValid = true;

  fields.forEach(field => {
    if (!validateField(field)) {
      isFormValid = false;
    }
  });

  return isFormValid;
}

function clearValidation(field) {
  field.classList.remove('is-valid', 'is-invalid');
  removeErrorMessage(field);
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', initFormValidation);
```

### Character Counter
```javascript
function initCharacterCounters() {
  const textareas = document.querySelectorAll('textarea[data-maxlength]');

  textareas.forEach(textarea => {
    const maxLength = parseInt(textarea.dataset.maxlength);
    const counter = textarea.parentNode.querySelector('.field__counter');

    textarea.addEventListener('input', () => {
      const currentLength = textarea.value.length;
      counter.textContent = `${currentLength}/${maxLength}`;

      if (currentLength > maxLength) {
        counter.classList.add('over-limit');
        textarea.classList.add('is-invalid');
      } else {
        counter.classList.remove('over-limit');
        textarea.classList.remove('is-invalid');
      }
    });
  });
}

document.addEventListener('DOMContentLoaded', initCharacterCounters);
```

## Responsive Design

### Mobile Optimizations
```css
@media (max-width: 767.98px) {
  /* Mejorar targets táctiles */
  input, textarea, select {
    min-height: 48px;
    font-size: 16px; /* Previene zoom en iOS */
  }

  /* Labels más grandes */
  .field__label {
    font-size: var(--text-base);
    font-weight: 600;
  }

  /* Espaciado mayor */
  .field {
    margin-bottom: var(--space-2);
  }

  /* Botones a ancho completo */
  .form__actions .btn {
    width: 100%;
  }
}
```

## Accesibilidad

### 1. Label Association
```html
<!-- ✅ Correcto - Label asociado -->
<label for="email" class="field__label">Email</label>
<input type="email" id="email" class="field__input" required>

<!-- ✅ Checkbox/Radio con label -->
<input type="checkbox" id="terms" class="checkbox__input">
<label for="terms" class="checkbox__label">Acepto términos</label>

<!-- ❌ Incorrecto - Label no asociado -->
<label>Email</label>
<input type="email">
```

### 2. ARIA Labels
```html
<input
  type="text"
  class="field__input"
  aria-label="Buscar productos"
  aria-describedby="search-help"
  aria-required="true"
>
<p id="search-help" class="field__hint">
  Introduce al menos 3 caracteres
</p>
```

### 3. Error Announcement
```html
<div class="field" aria-live="polite">
  <label for="email" class="field__label">Email</label>
  <input
    type="email"
    id="email"
    class="field__input is-invalid"
    aria-invalid="true"
    aria-describedby="email-error"
  >
  <p id="email-error" class="field__error" role="alert">
    Introduce un email válido
  </p>
</div>
```

### 4. Required Fields
```html
<label for="name" class="field__label">
  Nombre completo <span aria-label="obligatorio">*</span>
</label>
<input type="text" id="name" class="field__input" required aria-required="true">
```

### 5. Fieldset and Legend
```html
<fieldset>
  <legend>Información de Contacto</legend>

  <div class="field">
    <label for="email" class="field__label">Email</label>
    <input type="email" id="email" class="field__input">
  </div>

  <div class="field">
    <label for="phone" class="field__label">Teléfono</label>
    <input type="tel" id="phone" class="field__input">
  </div>
</fieldset>
```

## Testing

### Unit Tests
```javascript
describe('Form Validation', () => {
  test('validates required fields', () => {
    const field = document.createElement('input');
    field.required = true;
    field.value = '';

    const isValid = validateField(field);
    expect(isValid).toBe(false);
    expect(field.classList.contains('is-invalid')).toBe(true);
  });

  test('validates email format', () => {
    const field = document.createElement('input');
    field.type = 'email';
    field.value = 'invalid-email';

    const isValid = validateField(field);
    expect(isValid).toBe(false);
  });

  test('accepts valid email', () => {
    const field = document.createElement('input');
    field.type = 'email';
    field.value = 'user@example.com';

    const isValid = validateField(field);
    expect(isValid).toBe(true);
    expect(field.classList.contains('is-valid')).toBe(true);
  });
});
```

### Accessibility Tests
```javascript
describe('Form Accessibility', () => {
  test('has proper label associations', () => {
    cy.visit('/forms/auth');
    cy.injectAxe();

    // Verificar que todos los inputs tienen labels
    cy.get('input').each(($input) => {
      const id = $input.attr('id');
      const label = cy.get(`label[for="${id}"]`);
      label.should('exist');
    });

    // Verificar ARIA
    cy.checkA11y();
  });

  test('announces errors to screen readers', () => {
    cy.visit('/forms/register');

    // Enviar formulario vacío
    cy.get('button[type="submit"]').click();

    // Verificar que errores están presentes
    cy.get('.field__error').should('have.length.at.least', 1);

    // Verificar aria-invalid
    cy.get('.is-invalid').should('have.attr', 'aria-invalid', 'true');
  });
});
```

## Buenas Prácticas

### ✅ Hacer
```html
<!-- Usar label asociado -->
<label for="email" class="field__label">Email</label>
<input type="email" id="email" required>

<!-- Proporcionar placeholders descriptivos -->
<input type="search" placeholder="Buscar productos...">

<!-- Mostrar errores específicos -->
<input class="is-invalid">
<p class="field__error">El email debe contener @ y dominio</p>

<!-- Usar fieldset para grupos relacionados -->
<fieldset>
  <legend>Datos de facturación</legend>
  <!-- campos -->
</fieldset>

<!-- Indicar campos requeridos -->
<label>Nombre <span aria-label="required">*</span></label>
<input required aria-required="true">

<!-- Usar autocomplete -->
<input type="email" autocomplete="email">
<input type="password" autocomplete="current-password">

<!-- Mensajes de ayuda -->
<label for="bio">Biografía</label>
<textarea id="bio" aria-describedby="bio-help"></textarea>
<p id="bio-help" class="field__hint">Máximo 500 caracteres</p>
```

### ❌ Evitar
```html
<!-- No usar placeholder como label -->
<input placeholder="Email">

<!-- No errores vagos -->
<p class="field__error">Error</p>
<!-- Mejor: "El email debe ser válido" -->

<!-- No estilos inline -->
<input style="background: red; padding: 10px;">

<!-- No targets pequeños en móvil -->
<input style="height: 32px;">

<!-- No olvidar name attribute -->
<input type="email">  <!-- Debe tener name="email" -->

<!-- No usar div para formularios -->
<div class="form">
  <input type="text">  <!-- Usar <form> -->
</div>
```

## Casos de Uso

### 1. Multi-Step Form
```html
<form class="form form--multi-step">
  <div class="step-indicator">
    <span class="step is-active">1</span>
    <span class="step">2</span>
    <span class="step">3</span>
  </div>

  <div class="step step--active">
    <h3>Paso 1: Información Personal</h3>
    <div class="field">
      <label for="first-name">Nombre</label>
      <input id="first-name" required>
    </div>
    <div class="form__actions">
      <button type="button" class="btn btn--primary" data-next>
        Siguiente
      </button>
    </div>
  </div>

  <div class="step">
    <h3>Paso 2: Dirección</h3>
    <div class="form__actions">
      <button type="button" class="btn btn--ghost" data-prev>
        Anterior
      </button>
      <button type="button" class="btn btn--primary" data-next>
        Siguiente
      </button>
    </div>
  </div>

  <div class="step">
    <h3>Paso 3: Confirmación</h3>
    <div class="form__actions">
      <button type="button" class="btn btn--ghost" data-prev>
        Anterior
      </button>
      <button type="submit" class="btn btn--primary">
        Finalizar
      </button>
    </div>
  </div>
</form>
```

### 2. Filter Form (Catálogo)
```html
<form class="store-search" method="get">
  <div class="store-search__field-grid">
    <input
      type="search"
      name="q"
      class="field__input store-search__input-sm"
      placeholder="Buscar..."
      value="{{ request.GET.q }}"
    >

    <select name="type" class="field__input store-search__input-sm">
      <option value="">Tipo</option>
      <option value="cofre">Cofre</option>
      <option value="set">Set</option>
    </select>

    <input
      type="number"
      name="min_price"
      class="field__input store-search__input-narrow"
      placeholder="Min"
      value="{{ request.GET.min_price }}"
    >

    <input
      type="number"
      name="max_price"
      class="field__input store-search__input-narrow"
      placeholder="Max"
      value="{{ request.GET.max_price }}"
    >

    <button type="submit" class="btn btn--primary">
      Filtrar
    </button>
  </div>
</form>
```

## Referencias

### Archivos Relacionados
- `static/css/base.css` - Estilos base de inputs
- `static/css/components.css` - Formularios específicos
- `landing/forms.py` - Formularios Django
- `static/js/theme.js` - Validación dinámica

### Documentación Externa
- [WCAG 2.1 - Forms](https://www.w3.org/WAI/WCAG21/Understanding/info-and-relationships.html)
- [HTML5 Form Validation](https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/HTML5/Constraint_validation)
- [A11y Forms](https://webaim.org/techniques/forms/)

## Ver También
- [Botones](./botones.md)
- [Cards](./cards.md)
- [Modals](./modals.md)
- [Design System - Tokens](../design-system/tokens.md)
- [Design System - Colores](../design-system/colores.md)

/**
 * Language Selector
 * Maneja la interacción del selector de idiomas con dropdown
 */

(function() {
  'use strict';

  // Inicializar cuando el DOM esté listo
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  function init() {
    const selector = document.querySelector('.language-selector');
    if (!selector) return;

    const trigger = selector.querySelector('.language-selector__trigger');
    const dropdown = selector.querySelector('.language-selector__dropdown');

    if (!trigger || !dropdown) return;

    // Toggle dropdown al hacer click en el trigger
    trigger.addEventListener('click', function(e) {
      e.stopPropagation();
      const isExpanded = trigger.getAttribute('aria-expanded') === 'true';

      if (isExpanded) {
        closeDropdown();
      } else {
        openDropdown();
      }
    });

    // Cerrar dropdown al hacer click fuera
    document.addEventListener('click', function(e) {
      if (!selector.contains(e.target)) {
        closeDropdown();
      }
    });

    // Cerrar dropdown con tecla Escape
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape') {
        closeDropdown();
        trigger.focus();
      }
    });

    function openDropdown() {
      trigger.setAttribute('aria-expanded', 'true');
      dropdown.removeAttribute('hidden');

      // Focus en el primer botón activo o el primero disponible
      const activeOption = dropdown.querySelector('.language-selector__option.active');
      const firstOption = dropdown.querySelector('.language-selector__option');
      if (activeOption) {
        activeOption.focus();
      } else if (firstOption) {
        firstOption.focus();
      }
    }

    function closeDropdown() {
      trigger.setAttribute('aria-expanded', 'false');
      dropdown.setAttribute('hidden', '');
    }

    // Navegación con teclado dentro del dropdown
    dropdown.addEventListener('keydown', function(e) {
      const options = Array.from(dropdown.querySelectorAll('.language-selector__option'));
      const currentIndex = options.indexOf(document.activeElement);

      if (e.key === 'ArrowDown') {
        e.preventDefault();
        const nextIndex = currentIndex < options.length - 1 ? currentIndex + 1 : 0;
        options[nextIndex].focus();
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        const prevIndex = currentIndex > 0 ? currentIndex - 1 : options.length - 1;
        options[prevIndex].focus();
      } else if (e.key === 'Home') {
        e.preventDefault();
        options[0].focus();
      } else if (e.key === 'End') {
        e.preventDefault();
        options[options.length - 1].focus();
      }
    });

    // Cerrar dropdown al hacer click en un enlace de idioma
    const links = dropdown.querySelectorAll('.language-selector__option');
    links.forEach(link => {
      link.addEventListener('click', function() {
        closeDropdown();
      });
    });
  }
})();

// Tema: simple toggle por data-theme, persistente en localStorage
(function(){
  const root = document.documentElement;
  const KEY = 'theme';
  const setTheme = t=>{ root.setAttribute('data-theme', t); localStorage.setItem(KEY,t); };
  const getTheme = ()=> localStorage.getItem(KEY) || 'dark';

  const debounce = (fn,ms)=>{ let t; return (...a)=>{ clearTimeout(t); t=setTimeout(()=>fn(...a),ms);} };

  document.addEventListener('DOMContentLoaded',()=>{
    setTheme(getTheme());

    // Toggle de tema
    const themeToggle = document.querySelector('.theme-toggle__checkbox');
    if(themeToggle){
      themeToggle.checked = getTheme()==='light';
      themeToggle.addEventListener('change',()=> setTheme(themeToggle.checked?'light':'dark'));
    }

    // Navegación móvil
    const navToggle = document.querySelector('.nav-toggle');
    const navDrawer = document.querySelector('.nav-drawer');
    const body = document.body;
    const toggleNav = force=>{
      if(!navToggle || !navDrawer) return;
      const isOpen = force!==undefined ? !force : navToggle.getAttribute('aria-expanded')==='true';
      const next = !isOpen;
      navToggle.setAttribute('aria-expanded', String(next));
      navDrawer.classList.toggle('is-open', next);
      navDrawer.setAttribute('aria-hidden', String(!next));
      body.classList.toggle('nav-open', next);
      if(next){
        const firstLink = navDrawer.querySelector('a');
        firstLink && firstLink.focus();
      }else{
        navToggle.focus();
      }
    };
    if(navToggle && navDrawer){
      navToggle.setAttribute('aria-expanded','false');
      navToggle.addEventListener('click',()=>toggleNav());
      navDrawer.addEventListener('click',e=>{
        if(e.target === navDrawer) toggleNav(false);
        if(e.target instanceof HTMLElement && e.target.closest('a')) toggleNav(false);
      });
      document.addEventListener('keydown',e=>{
        if(e.key==='Escape' && navDrawer.classList.contains('is-open')) toggleNav(false);
      });
    }

    // Encoger header al hacer scroll
    const header = document.querySelector('.site-header');
    if(header){
      let ticking = false;
      const handleScroll = ()=>{
        const condense = window.scrollY > 89;
        header.classList.toggle('is-condensed', condense);
        ticking = false;
      };
      handleScroll();
      window.addEventListener('scroll',()=>{
        if(!ticking){
          window.requestAnimationFrame(handleScroll);
          ticking = true;
        }
      },{passive:true});
    }

    // Búsqueda accesible con debounce 233ms
    const list = document.querySelector('#search-list');
    const searchFields = Array.from(document.querySelectorAll('[data-search-input]'));
    if(list && searchFields.length){
      const items = Array.from(list.querySelectorAll('[role="option"]'));
      const applyFilter = value=>{
        const q = value.trim().toLowerCase();
        let visible = 0;
        items.forEach(it=>{
          const match = !q || it.textContent.toLowerCase().includes(q);
          it.style.display = match? 'block':'none';
          if(match) visible++;
        });
        const expanded = String(visible>0);
        searchFields.forEach(inp=>inp.setAttribute('aria-expanded', expanded));
      };
      const syncValue = (source,value)=>{
        searchFields.forEach(inp=>{ if(inp!==source) inp.value = value; });
      };
      searchFields.forEach(field=>{
        const run = debounce(()=>{
          syncValue(field,field.value);
          applyFilter(field.value);
        },233);
        field.addEventListener('input',run);
        field.addEventListener('focus',()=>field.setAttribute('aria-expanded','true'));
        field.addEventListener('keydown',e=>{
          if(e.key==='/' && !e.ctrlKey && !e.metaKey && !e.altKey){ e.preventDefault(); field.focus(); }
          if(e.key==='Escape'){ field.value=''; syncValue(field,''); applyFilter(''); field.setAttribute('aria-expanded','false'); }
        });
      });
      // acceso global con /
      document.addEventListener('keydown',e=>{
        if(e.key==='/' && !e.ctrlKey && !e.metaKey && !e.altKey && e.target instanceof HTMLElement && e.target.tagName!=='INPUT' && e.target.tagName!=='TEXTAREA' && !e.target.isContentEditable){
          e.preventDefault();
          const preferred = searchFields.find(inp=>inp.offsetParent!==null) || searchFields[0];
          preferred && preferred.focus();
        }
      });
    }
  });
})();

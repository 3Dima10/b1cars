(function () {
  const burger = document.getElementById('burgerBtn');
  const menu = document.getElementById('sideMenu');
  const backdrop = document.getElementById('sideMenuBackdrop');
  const closeBtn = document.getElementById('sideMenuClose');

  function openMenu() {
    menu.classList.add('open');
    backdrop.classList.add('open');
    burger.classList.add('open');
  }
  function closeMenu() {
    menu.classList.remove('open');
    backdrop.classList.remove('open');
    burger.classList.remove('open');
  }

  if (burger) {
    burger.addEventListener('click', function () {
      if (menu.classList.contains('open')) closeMenu(); else openMenu();
    });
  }
  if (closeBtn) closeBtn.addEventListener('click', closeMenu);
  if (backdrop) backdrop.addEventListener('click', closeMenu);

  // ---- Search / filters panel (home page) ----
  const filtersToggle = document.getElementById('filtersToggle');
  const filtersPanel = document.getElementById('filtersPanel');
  if (filtersToggle && filtersPanel) {
    const hasActiveFilters = filtersToggle.classList.contains('active');
    if (hasActiveFilters) {
      filtersPanel.classList.add('open');
      filtersToggle.setAttribute('aria-expanded', 'true');
    }
    filtersToggle.addEventListener('click', function () {
      const isOpen = filtersPanel.classList.toggle('open');
      filtersToggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    });
  }
})();

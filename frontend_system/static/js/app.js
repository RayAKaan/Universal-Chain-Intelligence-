class UCIApp {
  constructor() {
    this.api = new APIClient('/api');
    this.router = new Router();
    this.ws = new WebsocketClient();
    this.views = {};
    this.interval = null;
    this.navItems = [
      { key: 'dashboard', icon: '🏠', label: 'Dashboard' },
      { key: 'goals', icon: '🎯', label: 'Goals' },
      { key: 'capabilities', icon: '🧩', label: 'Capabilities' },
      { key: 'plans', icon: '🗺️', label: 'Plans' },
      { key: 'construction', icon: '🏗️', label: 'Construction' },
      { key: 'improvements', icon: '⚡', label: 'Improvements' },
      { key: 'safety', icon: '🛡️', label: 'Safety' },
      { key: 'console', icon: '💻', label: 'Console' },
      { key: 'settings', icon: '⚙️', label: 'Settings' },
      { key: 'knowledge', icon: '📚', label: 'Knowledge' },
      { key: 'notifications', icon: '🔔', label: 'Notifications' },
      { key: 'timeline', icon: '🕒', label: 'Timeline' },
      { key: 'health', icon: '💚', label: 'Health' },
    ];
  }

  init() {
    this._initNav();
    this._wireLayoutControls();
    this._initAtmospherics();
    this.views = {
      '/dashboard': new DashboardView(this),
      '/goals': new GoalConsoleView(this),
      '/capabilities': new CapabilityBrowserView(this),
      '/plans': new PlanViewerView(this),
      '/construction': new ConstructionWorkshopView(this),
      '/improvements': new ImprovementCenterView(this),
      '/safety': new SafetyPanelView(this),
      '/console': new SystemConsoleView(this),
      '/settings': new SettingsPanelView(this),
      '/knowledge': new KnowledgeExplorerView(this),
      '/notifications': new NotificationCenterView(this),
      '/timeline': new ActivityTimelineView(this),
      '/health': new HealthMonitorView(this),
    };

    this.router.onRouteChange((route) => this.navigate(route));
    this.navigate(this.router.getCurrentRoute());
    this._initModeBadge();
    this._initRealtime();
    this.startPolling();
  }

  async _initModeBadge() {
    const modeEl = document.getElementById('top-mode');
    if (!modeEl) return;
    try {
      const info = await this.api.getVersion();
      modeEl.textContent = `mode: ${info.mode || 'unknown'} • api ${info.api_version || 'n/a'}`;
    } catch (_error) {
      modeEl.textContent = 'mode: unavailable';
    }
  }

  _initRealtime() {
    this.ws.onEvent((event) => {
      const eventType = event?.event_type || '';
      if (eventType === 'API_MUTATION' || eventType.includes('PANIC') || eventType.includes('AUTONOMY')) {
        this.refresh();
      }
    });
    this.ws.start();
  }

  _initNav() {
    const sidebar = document.getElementById('sidebar');
    sidebar.innerHTML = `
      <div class="sidebar-header">Views</div>
      <nav class="sidebar-nav">
        ${this.navItems
          .map(
            (item) =>
              `<a class="nav-link" href="#/${item.key}" title="${item.label}" aria-label="${item.label}">
                <span class="nav-icon" aria-hidden="true">${item.icon}</span>
                <span class="nav-label">${item.label}</span>
              </a>`
          )
          .join('')}
      </nav>
    `;
  }

  _wireLayoutControls() {
    const menuBtn = document.getElementById('menu-toggle');
    if (menuBtn) {
      menuBtn.onclick = () => {
        if (window.innerWidth <= 900) {
          document.body.classList.toggle('sidebar-open-mobile');
          return;
        }
        document.body.classList.toggle('sidebar-collapsed');
      };
    }

    document.getElementById('view').onclick = () => {
      if (window.innerWidth <= 900) {
        document.body.classList.remove('sidebar-open-mobile');
      }
    };

    const orbToggle = document.getElementById('mobile-orb-toggle');
    if (orbToggle) {
      orbToggle.onclick = () => {
        document.body.classList.toggle('sidebar-open-mobile');
      };
    }

    window.addEventListener('scroll', () => {
      const topbar = document.querySelector('.topbar');
      if (topbar) topbar.classList.toggle('scrolled', window.scrollY > 8);
    });

    document.addEventListener('submit', (event) => {
      const text = event.target?.textContent?.toLowerCase() || '';
      if (text.includes('goal')) {
        this._triggerOrbRipple();
      }
    });
  }

  _initAtmospherics() {
    const cursor = document.getElementById('cursor-glow');
    if (cursor) {
      window.addEventListener('mousemove', (event) => {
        cursor.style.left = `${event.clientX}px`;
        cursor.style.top = `${event.clientY}px`;
      });
    }
  }

  _positionActiveIndicator() {
    const nav = document.querySelector('.sidebar-nav');
    const active = nav?.querySelector('.nav-link.active');
    if (!nav || !active) return;

    nav.style.setProperty('--active-top', `${active.offsetTop}px`);
    nav.style.setProperty('--active-height', `${active.offsetHeight}px`);
  }

  _setPresenceState(status) {
    const orb = document.getElementById('presence-indicator');
    if (!orb) return;

    const normalized = String(status || '').toLowerCase();
    orb.classList.toggle('thinking', normalized.includes('processing') || normalized.includes('active'));
    if (normalized.includes('degraded') || normalized.includes('error')) {
      orb.style.setProperty('--accent-blue', '#ff004c');
      return;
    }
    if (normalized.includes('optimal') || normalized.includes('healthy')) {
      orb.style.setProperty('--accent-blue', '#00ff9d');
      return;
    }
    orb.style.removeProperty('--accent-blue');
  }

  _triggerOrbRipple() {
    const ripple = document.getElementById('orb-ripple');
    if (!ripple) return;
    ripple.classList.remove('active');
    void ripple.offsetWidth;
    ripple.classList.add('active');
  }

  async navigate(route) {
    const view = this.views[route] || this.views['/dashboard'];
    const activeKey = route.replace('/', '');
    const activeMeta = this.navItems.find((item) => item.key === activeKey) || this.navItems[0];

    document.querySelectorAll('.nav-link').forEach((link) => {
      link.classList.toggle('active', link.getAttribute('href') === `#${route}`);
    });
    this._positionActiveIndicator();

    const titleEl = document.getElementById('current-view-title');
    if (titleEl) titleEl.textContent = activeMeta.label;

    try {
      await view.render();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } catch (error) {
      this.showNotification(error.message, 'error');
    }
  }

  refresh() {
    this.navigate(this.router.getCurrentRoute());
  }

  showNotification(message, type = 'info') {
    UIComponents.toast(message, type);
  }

  showModal(content) {
    UIComponents.modal('Details', content);
  }

  hideModal() {
    document.getElementById('modal').classList.add('hidden');
  }

  startPolling() {
    if (this.interval) clearInterval(this.interval);
    this.interval = setInterval(async () => {
      try {
        const status = await this.api.getStatus();
        document.getElementById('top-status').textContent = `${status.status} • ${status.active_goals} active goals`;
        this._setPresenceState(status.status);
      } catch (_error) {
        document.getElementById('top-status').textContent = 'Disconnected';
        this._setPresenceState('error');
      }
    }, 5000);
  }
}

window.addEventListener('DOMContentLoaded', () => {
  window.app = new UCIApp();
  app.init();
});

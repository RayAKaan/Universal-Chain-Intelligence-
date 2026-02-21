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
    this.startPolling();
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
  }

  async navigate(route) {
    const view = this.views[route] || this.views['/dashboard'];
    const activeKey = route.replace('/', '');
    const activeMeta = this.navItems.find((item) => item.key === activeKey) || this.navItems[0];

    document.querySelectorAll('.nav-link').forEach((link) => {
      link.classList.toggle('active', link.getAttribute('href') === `#${route}`);
    });

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
      } catch (_error) {
        document.getElementById('top-status').textContent = 'Disconnected';
      }
    }, 5000);
  }
}

window.addEventListener('DOMContentLoaded', () => {
  window.app = new UCIApp();
  app.init();
});

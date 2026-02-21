class HealthMonitorView {
  constructor(app) {
    this.app = app;
    this.chart = new SimpleChart();
  }

  async render() {
    const [h, r] = await Promise.all([
      this.app.api.get('/health/phases'),
      this.app.api.get('/health/resources'),
    ]);

    document.getElementById('view').innerHTML = `
      <div class='card'>
        <h3>Phase Health</h3>
        ${UIComponents.codeBlock(JSON.stringify(h.phases || {}, null, 2))}
      </div>
      <div class='card'>
        <h3>Resources</h3>
        <div id='gauge'></div>
      </div>
    `;

    const resources = r.resources || {};
    const cpu = resources.cpu ?? resources.cpu_percent ?? 0;
    this.chart.gaugeChart(document.getElementById('gauge'), cpu, 100);
  }
}

window.HealthMonitorView = HealthMonitorView;

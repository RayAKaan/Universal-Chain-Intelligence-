
class UCIApp{
  constructor(){this.api=new APIClient('/api');this.router=new Router();this.view=document.getElementById('view-root');this.views={};this.poll=null}
  async init(){
    this._boot();
    this._buildShell();
    this._bindPalette();
    this.views={'/dashboard':new DashboardView(this),'/goals':new GoalConsoleView(this),'/capabilities':new CapabilityBrowserView(this),'/plans':new PlanViewerView(this),'/construction':new ConstructionWorkshopView(this),'/improvements':new ImprovementCenterView(this),'/safety':new SafetyPanelView(this),'/console':new SystemConsoleView(this),'/settings':new SettingsPanelView(this),'/knowledge':new KnowledgeExplorerView(this),'/notifications':new NotificationCenterView(this),'/timeline':new ActivityTimelineView(this),'/health':new HealthMonitorView(this)};
    this.router.onChange=(r)=>this.navigate(r);
    this.navigate(this.router.current());
    this._startPolling();
    new ParticleSystem(document.getElementById('particle-canvas'));
  }
  async _boot(){const done=sessionStorage.getItem('uci-boot-done');const boot=document.getElementById('boot');if(done){boot.classList.add('hidden');document.getElementById('app-shell').classList.remove('hidden');return}
    const title='UNIVERSAL CHAIN INTELLIGENCE';const el=document.getElementById('boot-title');for(let i=0;i<title.length;i++){el.textContent+=title[i];await new Promise(r=>setTimeout(r,35))}
    await new Promise(r=>setTimeout(r,900));boot.classList.add('hidden');document.getElementById('app-shell').classList.remove('hidden');sessionStorage.setItem('uci-boot-done','1');document.body.onclick=()=>{boot.classList.add('hidden');document.getElementById('app-shell').classList.remove('hidden')}
  }
  _buildShell(){
    const header=document.getElementById('header');header.innerHTML=`<div class='brand'><div class='logo'></div><div><div class='name'>UCI</div><div class='tag'>Universal Chain Intelligence</div></div></div><div class='search-wrap'><input id='cmd-search' placeholder='Ask anything or search...'/><kbd>⌘K</kbd></div><div style='display:flex;gap:10px;align-items:center'><span>🔔</span><span id='health-chip' class='chip'>HEALTH</span><span id='aut-chip' class='chip'>GUIDED</span></div>`;
    const nav=[['/dashboard','◈','Dashboard'],['/goals','◎','Goals'],['/capabilities','◇','Capabilities'],['/plans','◆','Plans'],['/construction','⚡','Construction'],['/improvements','△','Improvements'],['/safety','⛨','Safety'],['/console','▣','Console'],['/settings','⚙','Settings'],['/knowledge','◉','Knowledge'],['/timeline','♦','Timeline'],['/health','♡','Health']];
    document.getElementById('sidebar').innerHTML=nav.map(([p,i,t])=>`<a class='nav-item' href='#${p}'><span>${i}</span><span>${t}</span></a>`).join('')+`<div style='position:sticky;bottom:0;padding-top:12px'><span class='status-dot healthy'></span> <small>ONLINE</small></div>`;
  }
  _bindPalette(){window.addEventListener('keydown',e=>{if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='k'){e.preventDefault();this.togglePalette()}})}
  togglePalette(){const p=document.getElementById('command-palette');if(p.classList.contains('hidden')){p.classList.remove('hidden');p.innerHTML=`<div class='modal-content'><input class='input' id='palette-input' placeholder='Type a command or route'/><div id='palette-results' style='margin-top:10px'></div></div>`;const inp=document.getElementById('palette-input');inp.focus();inp.oninput=()=>{const q=inp.value.toLowerCase();const items=Object.keys(this.views).filter(x=>x.includes(q));document.getElementById('palette-results').innerHTML=items.map(i=>`<div class='chip' data-route='${i}'>${i}</div>`).join('')||'<small>No match</small>';document.querySelectorAll('[data-route]').forEach(x=>x.onclick=()=>{this.router.go(x.dataset.route);this.togglePalette()})}}else{p.classList.add('hidden')}}
  async navigate(route){const v=this.views[route]||this.views['/dashboard'];document.querySelectorAll('.nav-item').forEach(n=>n.classList.toggle('active',n.getAttribute('href')===`#${route}`));const wrap=document.getElementById('view-transition');wrap.style.opacity='0';await new Promise(r=>setTimeout(r,150));await v.mount();wrap.style.opacity='1';document.querySelectorAll('.card').forEach(c=>SceneManager.addTilt(c))}
  _startPolling(){if(this.poll)clearInterval(this.poll);this.poll=setInterval(async()=>{try{const s=await this.api.getStatus();document.getElementById('health-chip').textContent=`${Math.round((s.score||0)*100)}%`;document.getElementById('status-strip').innerHTML=`${Object.entries(s.phases||{}).map(([k,v])=>`<span><span class='status-dot ${v}'></span> ${k}</span>`).join(' | ')} | ⏱ ${(s.uptime_seconds/3600).toFixed(1)}h | ◎ ${s.active_goals} active | CPU ${s.resources?.cpu||0}% RAM ${s.resources?.memory||0}%`;}catch(e){UIComponents.toast(e.message,'error')}},5000)}
}
window.addEventListener('DOMContentLoaded',()=>{window.app=new UCIApp();app.init()});

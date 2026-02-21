
class UCIApp{
 constructor(){this.api=new APIClient('/api');this.router=new Router();this.ws=new WebsocketClient();this.views={};this.interval=null}
 init(){
  this._initNav();
  this.views={
   '/dashboard':new DashboardView(this),'/goals':new GoalConsoleView(this),'/capabilities':new CapabilityBrowserView(this),'/plans':new PlanViewerView(this),
   '/construction':new ConstructionWorkshopView(this),'/improvements':new ImprovementCenterView(this),'/safety':new SafetyPanelView(this),'/console':new SystemConsoleView(this),
   '/settings':new SettingsPanelView(this),'/knowledge':new KnowledgeExplorerView(this),'/notifications':new NotificationCenterView(this),'/timeline':new ActivityTimelineView(this),'/health':new HealthMonitorView(this)
  };
  this.router.onRouteChange((r)=>this.navigate(r));
  this.navigate(this.router.getCurrentRoute());
  this.startPolling();
 }
 _initNav(){const items=['dashboard','goals','capabilities','plans','construction','improvements','safety','console','settings','knowledge','notifications','timeline','health'];document.getElementById('sidebar').innerHTML=items.map(i=>`<a class='nav-link' href='#/${i}'>${i}</a>`).join('')}
 async navigate(route){const v=this.views[route]||this.views['/dashboard'];document.querySelectorAll('.nav-link').forEach(a=>a.classList.toggle('active',a.getAttribute('href')===`#${route}`));try{await v.render()}catch(e){this.showNotification(e.message,'error')}}
 refresh(){this.navigate(this.router.getCurrentRoute())}
 showNotification(message,type='info'){UIComponents.toast(message,type)}
 showModal(content){UIComponents.modal('Details',content)} hideModal(){document.getElementById('modal').classList.add('hidden')}
 startPolling(){if(this.interval)clearInterval(this.interval);this.interval=setInterval(async()=>{try{const s=await this.api.getStatus();document.getElementById('top-status').textContent=`${s.status} | goals ${s.active_goals}`;}catch(e){}},5000)}
}
window.addEventListener('DOMContentLoaded',()=>{window.app=new UCIApp();app.init()});


class APIClient{
  constructor(base='/api'){this.base=base}
  async request(method,path,data=null,params=null){
    const q=params?`?${new URLSearchParams(params)}`:''
    const res=await fetch(`${this.base}${path}${q}`,{method,headers:{'Content-Type':'application/json'},body:data?JSON.stringify(data):undefined})
    if(!res.ok){let msg='Request failed';try{const j=await res.json();msg=j.error||msg}catch{}throw new Error(msg)}
    return res.json()
  }
  get(p,params){return this.request('GET',p,null,params)} post(p,d){return this.request('POST',p,d)}
  submitGoal(goal,priority){return this.post('/goals',{goal,priority})}
  getGoals(filters){return this.get('/goals',filters)} getGoal(id){return this.get(`/goals/${id}`)}
  cancelGoal(id){return this.post(`/goals/${id}/cancel`,{})} pauseGoal(id){return this.post(`/goals/${id}/pause`,{})} resumeGoal(id){return this.post(`/goals/${id}/resume`,{})}
  getStatus(){return this.get('/status')} getDashboard(){return this.get('/status/dashboard')} getHealth(){return this.get('/status/health')}
  getCapabilities(f){return this.get('/capabilities',f)} getCapability(id){return this.get(`/capabilities/${id}`)} triggerDiscovery(){return this.post('/capabilities/discover',{})}
  getPlans(){return this.get('/plans')} getPlan(id){return this.get(`/plans/${id}`)} getPlanGraph(id){return this.get(`/plans/${id}/graph`)}
  build(spec){return this.post('/construction/build',{spec})} getTemplates(){return this.get('/construction/templates')}
  getImprovements(){return this.get('/improvements')} getBottlenecks(){return this.get('/improvements/bottlenecks')} getOpportunities(){return this.get('/improvements/opportunities')} triggerImprovementCycle(){return this.post('/improvements/cycle',{})}
  getSafetyStatus(){return this.get('/safety/status')} getAuditTrail(limit=100,offset=0){return this.get('/safety/audit',{limit,offset})} getTrust(){return this.get('/safety/trust')} getAlignment(){return this.get('/safety/alignment')}
  panic(reason){return this.post('/safety/emergency/panic',{reason})}
  getSettings(){return this.get('/settings')} setAutonomy(level){return this.post('/settings/autonomy',{level})}
  getKnowledge(q){return this.get('/knowledge',q)}
  getNotifications(unread){return this.get('/notifications',unread?{unread:'true'}:null)}
  getTimeline(params){return this.get('/timeline',params)}
  execute(command){return this.post('/console/execute',{command})}
}
window.APIClient=APIClient;


class APIClient{constructor(baseUrl='/api'){this.baseUrl=baseUrl}
async get(path,params){const q=params?`?${new URLSearchParams(params)}`:'';const r=await fetch(`${this.baseUrl}${path}${q}`);if(!r.ok)throw new Error(await r.text());return r.json()}
async post(path,data){const r=await fetch(`${this.baseUrl}${path}`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data||{})});if(!r.ok)throw new Error(await r.text());return r.json()}
async put(path,data){return this.post(path,data)} async delete(path){return this.post(path,{})}
submitGoal(goalText,priority){return this.post('/goals',{goal:goalText,priority})}
getGoals(filters){return this.get('/goals',filters)} getGoal(id){return this.get(`/goals/${id}`)} cancelGoal(id){return this.post(`/goals/${id}/cancel`,{})}
getStatus(){return this.get('/status')} getDashboard(){return this.get('/status/dashboard')} getHealth(){return this.get('/status/health')}
getCapabilities(filters){return this.get('/capabilities',filters)} getCapability(id){return this.get(`/capabilities/${id}`)} triggerDiscovery(){return this.post('/capabilities/discover',{})}
getPlans(){return this.get('/plans')} getPlan(id){return this.get(`/plans/${id}`)} getPlanGraph(id){return this.get(`/plans/${id}/graph`)}
getImprovements(){return this.get('/improvements')} getBottlenecks(){return this.get('/improvements/bottlenecks')} getOpportunities(){return this.get('/improvements/opportunities')} triggerImprovementCycle(){return this.post('/improvements/cycle',{})}
getSafetyStatus(){return this.get('/safety/status')} getAuditTrail(limit=100,offset=0){return this.get('/safety/audit',{limit,offset})} getTrustLevel(){return this.get('/safety/trust')} getAlignmentScore(){return this.get('/safety/alignment')}
getSettings(){return this.get('/settings')} setAutonomyLevel(level){return this.post('/settings/autonomy',{level})}
queryKnowledge(query){return this.get('/knowledge',query)}
executeCommand(command){return this.post('/console/execute',{command})}
askSystem(question){return this.get('/system/ask',{q:question})}
getSystemInfo(){return this.get('/system/info')}
handleError(error){console.error(error);UIComponents.toast(error.message||'Request failed','error')}
}
window.APIClient=APIClient;

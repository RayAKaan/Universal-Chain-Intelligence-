
class Router{constructor(){this.routes={};this.cb=null;window.addEventListener('hashchange',()=>this._emit())}
register(path,view){this.routes[path]=view}
navigate(path){location.hash=path}
getCurrentRoute(){return location.hash.replace('#','')||'/dashboard'}
onRouteChange(cb){this.cb=cb}
_emit(){if(this.cb)this.cb(this.getCurrentRoute())}
}
window.Router=Router;

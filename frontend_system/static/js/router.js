
class Router{
  constructor(){this.routes={};this.onChange=null;window.addEventListener('hashchange',()=>this.emit())}
  register(path,view){this.routes[path]=view}
  current(){return location.hash.replace('#','')||'/dashboard'}
  go(path){location.hash=path}
  emit(){this.onChange&&this.onChange(this.current())}
}
window.Router=Router;


class UIComponents{
 static statusBadge(s){const cls=s==='healthy'||s==='completed'?'badge-healthy':s==='failed'||s==='unhealthy'?'badge-unhealthy':'badge-degraded';return `<span class='badge ${cls}'>${s}</span>`}
 static metricCard(title,val,trend=''){return `<article class='card kpi'><div class='metric-value' data-animate>${val}</div><div class='metric-label'>${title}</div><div class='metric-trend'>${trend}</div></article>`}
 static table(headers,rows,sortable=true){const id='t'+Math.random().toString(36).slice(2,8);return `<table class='table' id='${id}'><thead><tr>${headers.map((h,i)=>`<th data-col='${i}'>${h}${sortable?' ↕':''}</th>`).join('')}</tr></thead><tbody>${rows.map(r=>`<tr>${r.map(c=>`<td>${c}</td>`).join('')}</tr>`).join('')}</tbody></table>`}
 static toast(msg,type='info'){const c=document.getElementById('toast-container');const el=document.createElement('div');el.className='toast';el.textContent=msg;el.style.setProperty('--bar',type);c.prepend(el);setTimeout(()=>el.remove(),5000)}
 static modal(title,content,actions=''){const m=document.getElementById('modal-container');m.innerHTML=`<div class='modal-content'><h3>${title}</h3>${content}<div style='margin-top:12px'>${actions||"<button class='btn' id='modal-close'>Close</button>"}</div></div>`;m.classList.remove('hidden');const c=document.getElementById('modal-close');if(c)c.onclick=()=>m.classList.add('hidden')}
 static progress(v){return `<div class='progress'><span style='width:${v}%'></span></div>`}
 static timeline(events){return `<div>${events.map(e=>`<div class='card'><div style='display:flex;justify-content:space-between'><span>${e.event_type||e.type}</span><small>${Utils.timeAgo(e.timestamp)}</small></div><div>${e.details||''}</div></div>`).join('')}</div>`}
 static empty(msg,action=''){return `<div class='card'><p>${msg}</p>${action}</div>`}
}
window.UIComponents=UIComponents;


class UIComponents{
 static statCard(title,value,trend,icon='📊'){return `<div class="card"><div>${icon} ${title}</div><div class="stat-value">${value}</div><div class="muted">${trend||''}</div></div>`}
 static badge(text,color='healthy'){return `<span class="badge ${color}">${text}</span>`}
 static statusDot(status){const c=status==='healthy'?'healthy':status==='degraded'?'degraded':'unhealthy';return `<span class="phase-dot ${c}"></span>`}
 static toast(message,type='info',duration=3000){const c=document.getElementById('toast-container');const el=document.createElement('div');el.className='toast';el.textContent=message;c.appendChild(el);setTimeout(()=>el.remove(),duration)}
 static modal(title,content,actions=''){const m=document.getElementById('modal');document.getElementById('modal-body').innerHTML=`<h3>${title}</h3>${content}<div>${actions}</div>`;m.classList.remove('hidden')}
 static confirmDialog(message,onConfirm,onCancel){if(confirm(message)){onConfirm&&onConfirm()}else{onCancel&&onCancel()}}
 static table(headers,rows){const th=headers.map(h=>`<th>${h}</th>`).join('');const tr=rows.map(r=>`<tr>${r.map(c=>`<td>${c}</td>`).join('')}</tr>`).join('');return `<table class='table'><thead><tr>${th}</tr></thead><tbody>${tr}</tbody></table>`}
 static tabs(tabs,active){return `<div class='tabs'>${tabs.map(t=>`<button class='tab ${t===active?'active':''}' data-tab='${t}'>${t}</button>`).join('')}</div>`}
 static searchBar(ph='Search'){return `<input class='input' placeholder='${ph}'/>`}
 static emptyState(message='No data'){return `<div class='card'>${message}</div>`}
 static loadingSpinner(){return `<span class='spinner'></span>`}
 static progressBar(value,max=100,label=''){const p=Math.min(100,Math.round((value/max)*100));return `<div>${label} ${p}%<div class='progress'><span style='width:${p}%'></span></div></div>`}
 static timeline(events){return `<div>${events.map(e=>`<div class='card'><b>${e.event_type||e.type}</b> <small>${Utils.timeAgo(e.timestamp)}</small><div>${e.details||''}</div></div>`).join('')}</div>`}
 static codeBlock(code){return `<pre class='terminal'>${String(code).replace(/</g,'&lt;')}</pre>`}
 static keyValue(pairs){return this.table(['Key','Value'],Object.entries(pairs))}
}
window.UIComponents=UIComponents;

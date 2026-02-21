
class SimpleChart{
 lineChart(el,data,opt={}){const w=opt.w||420,h=opt.h||180,max=Math.max(...data.map(d=>d.value),1);const pts=data.map((d,i)=>({x:(i/(data.length-1||1))*w,y:h-(d.value/max*h)}));let d=`M ${pts[0]?.x||0} ${pts[0]?.y||0}`;for(let i=1;i<pts.length;i++){const p=pts[i-1],c=pts[i];const mx=(p.x+c.x)/2;d+=` C ${mx} ${p.y}, ${mx} ${c.y}, ${c.x} ${c.y}`}
 const area=d+` L ${w} ${h} L 0 ${h} Z`;el.innerHTML=`<svg viewBox='0 0 ${w} ${h}'><defs><linearGradient id='g1' x1='0' x2='0' y1='0' y2='1'><stop offset='0%' stop-color='rgba(0,212,255,.25)'/><stop offset='100%' stop-color='rgba(0,212,255,0)'/></linearGradient></defs><path d='${area}' fill='url(#g1)'/><path d='${d}' stroke='var(--accent-cyan)' stroke-width='2' fill='none'/></svg>`}
 barChart(el,data){el.innerHTML=data.map(x=>`<div>${x.label} ${x.value}%${UIComponents.progress(x.value)}</div>`).join('')}
 donutChart(el,data){const total=data.reduce((a,b)=>a+b.value,0)||1;let cur=0;const r=42,c=50;const seg=data.map(s=>{const a1=cur/total*2*Math.PI,a2=(cur+s.value)/total*2*Math.PI;cur+=s.value;const x1=c+r*Math.cos(a1),y1=c+r*Math.sin(a1),x2=c+r*Math.cos(a2),y2=c+r*Math.sin(a2),laf=(a2-a1)>Math.PI?1:0;return `<path d='M ${c} ${c} L ${x1} ${y1} A ${r} ${r} 0 ${laf} 1 ${x2} ${y2} Z' fill='${s.color}'/>`}).join('');el.innerHTML=`<svg viewBox='0 0 100 100'>${seg}<circle cx='50' cy='50' r='22' fill='var(--depth-2)'/><text x='50' y='53' text-anchor='middle' class='donut-center'>${total}</text></svg>`}
 gaugeChart(el,val,max=100){const p=Utils.pct(val,max);el.innerHTML=`<div class='gauge'><div class='metric-value'>${p}%</div>${UIComponents.progress(p)}</div>`}
 sparkline(el,data){this.lineChart(el,data,{w:100,h:24})}
 progressBar(el,v,m=100){el.innerHTML=UIComponents.progress(Utils.pct(v,m))}
 timelineChart(el,events){el.innerHTML=UIComponents.timeline(events)}
}
window.SimpleChart=SimpleChart;

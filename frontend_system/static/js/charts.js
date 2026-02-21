
class SimpleChart{
 barChart(container,data){container.innerHTML=data.map(d=>`<div>${d.label}: ${d.value}<div class='progress'><span style='width:${d.value}%'></span></div></div>`).join('')}
 lineChart(container,data){const w=320,h=120;const max=Math.max(...data,1);const pts=data.map((v,i)=>`${(i/(data.length-1||1))*w},${h-(v/max*h)}`).join(' ');container.innerHTML=`<svg viewBox='0 0 ${w} ${h}'><polyline fill='none' stroke='#58a6ff' stroke-width='2' points='${pts}'/></svg>`}
 donutChart(container,data){const total=data.reduce((a,b)=>a+b.value,0)||1;let a=0;const c=42,r=36;const seg=data.map(d=>{const p=d.value/total;const a2=a+p*Math.PI*2;const x1=c+r*Math.cos(a),y1=c+r*Math.sin(a),x2=c+r*Math.cos(a2),y2=c+r*Math.sin(a2),laf=p>0.5?1:0;const path=`M ${c} ${c} L ${x1} ${y1} A ${r} ${r} 0 ${laf} 1 ${x2} ${y2} Z`;a=a2;return `<path d="${path}" fill="${d.color||'#58a6ff'}"/>`}).join('');container.innerHTML=`<svg viewBox='0 0 84 84'>${seg}<circle cx='42' cy='42' r='20' fill='#0d1117'/></svg>`}
 gaugeChart(container,value,max=100){const p=Math.min(1,value/max);container.innerHTML=`<div>${Math.round(p*100)}%</div><div class='progress'><span style='width:${p*100}%'></span></div>`}
 sparkline(container,data){this.lineChart(container,data)}
 progressBar(container,value,max=100){container.innerHTML=UIComponents.progressBar(value,max)}
 timelineChart(container,events){container.innerHTML=UIComponents.timeline(events)}
}
window.SimpleChart=SimpleChart;

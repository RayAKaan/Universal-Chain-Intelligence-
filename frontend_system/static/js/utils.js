
window.Utils={
 fmtNum:n=>Number(n||0).toLocaleString(),
 isoNow:()=>new Date().toISOString(),
 timeAgo:iso=>{try{const d=new Date(iso);const s=(Date.now()-d.getTime())/1000;if(s<60)return `${Math.floor(s)}s`;if(s<3600)return `${Math.floor(s/60)}m`;if(s<86400)return `${Math.floor(s/3600)}h`;return `${Math.floor(s/86400)}d`}catch{return 'n/a'}},
 debounce(fn,ms=300){let t;return(...a)=>{clearTimeout(t);t=setTimeout(()=>fn(...a),ms)}},
 pct:(v,m=100)=>Math.max(0,Math.min(100,Math.round((v/m)*100))),
 sortRows(rows,col,asc=true){return [...rows].sort((a,b)=>String(a[col]).localeCompare(String(b[col]))*(asc?1:-1))}
};

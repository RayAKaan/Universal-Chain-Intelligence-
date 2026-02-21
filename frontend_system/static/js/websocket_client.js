class WebsocketClient{constructor(){this.seq=0}async poll(){const r=await fetch('/ws');return r.json()}};window.WebsocketClient=WebsocketClient;

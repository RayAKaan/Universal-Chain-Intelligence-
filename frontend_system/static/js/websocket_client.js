class WebsocketClient {
  constructor() {
    this.seq = 0;
    this.listeners = [];
    this.running = false;
  }

  onEvent(callback) {
    this.listeners.push(callback);
  }

  async poll(timeout = 30, events = ['*']) {
    const params = new URLSearchParams({
      since: String(this.seq),
      timeout: String(timeout),
      events: events.join(','),
    });
    const response = await fetch(`/ws?${params.toString()}`);
    if (!response.ok) throw new Error(await response.text());
    const payload = await response.json();
    this.seq = payload.next_sequence || this.seq;
    return payload;
  }

  start() {
    if (this.running) return;
    this.running = true;

    const loop = async () => {
      while (this.running) {
        try {
          const payload = await this.poll();
          (payload.events || []).forEach((event) => {
            this.listeners.forEach((listener) => listener(event));
          });
        } catch (_error) {
          await new Promise((resolve) => setTimeout(resolve, 1000));
        }
      }
    };

    loop();
  }

  stop() {
    this.running = false;
  }
}

window.WebsocketClient = WebsocketClient;

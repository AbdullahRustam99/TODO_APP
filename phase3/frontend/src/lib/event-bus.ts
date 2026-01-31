// A simple event emitter for cross-component communication

type EventHandler = (...args: any[]) => void;

interface Events {
  [key: string]: EventHandler[];
}

class EventEmitter {
  private events: Events = {};

  on(event: string, listener: EventHandler) {
    if (!this.events[event]) {
      this.events[event] = [];
    }
    this.events[event].push(listener);
  }

  off(event: string, listener: EventHandler) {
    if (!this.events[event]) return;

    this.events[event] = this.events[event].filter(l => l !== listener);
  }

  emit(event: string, ...args: any[]) {
    if (!this.events[event]) return;

    this.events[event].forEach(listener => listener(...args));
  }
}

export const eventBus = new EventEmitter();
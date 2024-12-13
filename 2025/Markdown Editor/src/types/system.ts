export interface SystemStatus {
  isReady: boolean;
  components: {
    editor: boolean;
    preview: boolean;
    storage: boolean;
    autosave: boolean;
  };
  performance: {
    renderTime: number;
    memoryUsage: number;
  };
}

export interface SystemHealth {
  status: 'healthy' | 'degraded' | 'error';
  timestamp: number;
  diagnostics: {
    componentId: string;
    status: 'ok' | 'warning' | 'error';
    message?: string;
  }[];
}
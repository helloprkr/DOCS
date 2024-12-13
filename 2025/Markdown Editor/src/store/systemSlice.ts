import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { SystemStatus, SystemHealth } from '@/types/system';

interface SystemState {
  status: SystemStatus;
  health: SystemHealth;
  lastCheck: number;
}

const initialState: SystemState = {
  status: {
    isReady: false,
    components: {
      editor: false,
      preview: false,
      storage: false,
      autosave: false,
    },
    performance: {
      renderTime: 0,
      memoryUsage: 0,
    },
  },
  health: {
    status: 'healthy',
    timestamp: Date.now(),
    diagnostics: [],
  },
  lastCheck: 0,
};

export const systemSlice = createSlice({
  name: 'system',
  initialState,
  reducers: {
    updateComponentStatus: (
      state,
      action: PayloadAction<{ component: keyof SystemStatus['components']; status: boolean }>
    ) => {
      state.status.components[action.payload.component] = action.payload.status;
      state.status.isReady = Object.values(state.status.components).every(Boolean);
    },
    updatePerformance: (
      state,
      action: PayloadAction<Partial<SystemStatus['performance']>>
    ) => {
      state.status.performance = { ...state.status.performance, ...action.payload };
    },
    updateHealth: (state, action: PayloadAction<SystemHealth>) => {
      state.health = action.payload;
      state.lastCheck = Date.now();
    },
  },
});

export const { updateComponentStatus, updatePerformance, updateHealth } = systemSlice.actions;
export default systemSlice.reducer;
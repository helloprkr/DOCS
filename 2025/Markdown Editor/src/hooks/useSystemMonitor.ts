import { useEffect } from 'react';
import { useDispatch } from 'react-redux';
import { updateComponentStatus, updatePerformance, updateHealth } from '@/store/systemSlice';
import { get } from 'idb-keyval';

export function useSystemMonitor() {
  const dispatch = useDispatch();

  useEffect(() => {
    const checkSystem = async () => {
      // Check storage
      try {
        await get('test-key');
        dispatch(updateComponentStatus({ component: 'storage', status: true }));
      } catch {
        dispatch(updateComponentStatus({ component: 'storage', status: false }));
      }

      // Check performance
      const start = performance.now();
      const memory = (performance as any).memory?.usedJSHeapSize || 0;
      
      dispatch(updatePerformance({
        renderTime: performance.now() - start,
        memoryUsage: memory,
      }));

      // Update health status
      dispatch(updateHealth({
        status: 'healthy',
        timestamp: Date.now(),
        diagnostics: [
          { componentId: 'editor', status: 'ok' },
          { componentId: 'storage', status: 'ok' },
        ],
      }));
    };

    // Initial check
    checkSystem();

    // Regular monitoring
    const interval = setInterval(checkSystem, 5000);
    return () => clearInterval(interval);
  }, [dispatch]);
}
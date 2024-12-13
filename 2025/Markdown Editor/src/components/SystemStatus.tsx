import { useSelector } from 'react-redux';
import { RootState } from '@/store/store';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { Activity, CheckCircle, AlertCircle } from 'lucide-react';

export function SystemStatus() {
  const { status, health } = useSelector((state: RootState) => state.system);

  const getStatusColor = (isActive: boolean) =>
    isActive ? 'bg-green-500' : 'bg-red-500';

  const getHealthIcon = () => {
    switch (health.status) {
      case 'healthy':
        return <CheckCircle className="h-4 w-4 text-green-500" />;
      case 'degraded':
        return <Activity className="h-4 w-4 text-yellow-500" />;
      case 'error':
        return <AlertCircle className="h-4 w-4 text-red-500" />;
    }
  };

  const completionPercentage =
    (Object.values(status.components).filter(Boolean).length /
      Object.values(status.components).length) *
    100;

  return (
    <div className="fixed bottom-4 right-4 p-4 bg-background/80 backdrop-blur-sm rounded-lg shadow-lg border">
      <div className="flex items-center gap-2 mb-2">
        {getHealthIcon()}
        <span className="font-medium">System Status</span>
      </div>
      
      <div className="space-y-2">
        <Progress value={completionPercentage} className="h-2" />
        
        <div className="flex gap-2">
          {Object.entries(status.components).map(([key, value]) => (
            <Badge
              key={key}
              variant={value ? 'default' : 'destructive'}
              className="text-xs"
            >
              {key}
            </Badge>
          ))}
        </div>
      </div>
    </div>
  );
}
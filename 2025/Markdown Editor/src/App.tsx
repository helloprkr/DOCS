import { Editor } from '@/components/Editor';
import { SystemStatus } from '@/components/SystemStatus';
import { useSystemMonitor } from '@/hooks/useSystemMonitor';

function App() {
  useSystemMonitor();

  return (
    <>
      <Editor />
      <SystemStatus />
    </>
  );
}

export default App;
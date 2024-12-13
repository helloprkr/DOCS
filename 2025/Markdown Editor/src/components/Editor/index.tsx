import { Panel, PanelGroup, PanelResizeHandle } from 'react-resizable-panels';
import { EditorPane } from './EditorPane';
import { PreviewPane } from './PreviewPane';
import { Toolbar } from './Toolbar';
import { useAutosave } from '@/hooks/useAutosave';

export function Editor() {
  useAutosave();

  return (
    <div className="h-screen bg-background flex flex-col">
      <Toolbar />
      <div className="flex-1">
        <PanelGroup direction="horizontal">
          <Panel defaultSize={50}>
            <EditorPane />
          </Panel>
          <PanelResizeHandle className="w-2 bg-border hover:bg-primary/20 transition-colors" />
          <Panel defaultSize={50}>
            <PreviewPane />
          </Panel>
        </PanelGroup>
      </div>
    </div>
  );
}
import React from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Panel, PanelGroup, PanelResizeHandle } from 'react-resizable-panels';
import { Textarea } from '@/components/ui/textarea';
import { updateContent } from '@/store/editorSlice';
import { RootState } from '@/store/store';
import { useAutosave } from '@/hooks/useAutosave';
import { marked } from 'marked';

export function Editor() {
  const dispatch = useDispatch();
  const content = useSelector((state: RootState) => state.editor.content);
  useAutosave();

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    dispatch(updateContent(e.target.value));
  };

  return (
    <div className="h-screen bg-background">
      <PanelGroup direction="horizontal">
        <Panel defaultSize={50}>
          <div className="h-full p-4">
            <Textarea
              className="h-full w-full resize-none font-mono"
              value={content}
              onChange={handleChange}
              placeholder="Start writing..."
            />
          </div>
        </Panel>
        <PanelResizeHandle className="w-2 bg-border hover:bg-primary/20 transition-colors" />
        <Panel defaultSize={50}>
          <div 
            className="h-full p-4 prose prose-sm max-w-none dark:prose-invert"
            dangerouslySetInnerHTML={{ __html: marked(content) }}
          />
        </Panel>
      </PanelGroup>
    </div>
  );
}
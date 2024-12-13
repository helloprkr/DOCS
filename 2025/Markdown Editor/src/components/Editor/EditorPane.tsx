import React from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Textarea } from '@/components/ui/textarea';
import { updateContent } from '@/store/editorSlice';
import { RootState } from '@/store/store';

export function EditorPane() {
  const dispatch = useDispatch();
  const content = useSelector((state: RootState) => state.editor.content);

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    dispatch(updateContent(e.target.value));
  };

  return (
    <div className="h-full p-4">
      <Textarea
        className="h-full w-full resize-none font-mono"
        value={content}
        onChange={handleChange}
        placeholder="Start writing..."
      />
    </div>
  );
}
import { useSelector } from 'react-redux';
import { RootState } from '@/store/store';
import { marked } from 'marked';

export function PreviewPane() {
  const content = useSelector((state: RootState) => state.editor.content);

  return (
    <div 
      className="h-full p-4 prose prose-sm max-w-none dark:prose-invert overflow-auto"
      dangerouslySetInnerHTML={{ __html: marked(content) }}
    />
  );
}
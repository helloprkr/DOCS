import { useEffect, useCallback } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import { set } from 'idb-keyval';
import { RootState } from '@/store/store';
import { markSaved } from '@/store/editorSlice';
import { updateComponentStatus } from '@/store/systemSlice';

const AUTOSAVE_INTERVAL = 30000; // 30 seconds

export function useAutosave() {
  const dispatch = useDispatch();
  const { content, isDirty } = useSelector((state: RootState) => state.editor);

  const saveContent = useCallback(async () => {
    if (isDirty) {
      try {
        await set('editor-content', content);
        dispatch(markSaved());
        dispatch(updateComponentStatus({ component: 'autosave', status: true }));
      } catch (error) {
        dispatch(updateComponentStatus({ component: 'autosave', status: false }));
        console.error('Autosave failed:', error);
      }
    }
  }, [content, isDirty, dispatch]);

  useEffect(() => {
    const timer = setInterval(saveContent, AUTOSAVE_INTERVAL);
    return () => clearInterval(timer);
  }, [saveContent]);
}
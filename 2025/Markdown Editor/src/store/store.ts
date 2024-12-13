import { configureStore } from '@reduxjs/toolkit';
import editorReducer from './editorSlice';
import systemReducer from './systemSlice';
import documentsReducer from './documentsSlice';

export const store = configureStore({
  reducer: {
    editor: editorReducer,
    system: systemReducer,
    documents: documentsReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: false,
    }),
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
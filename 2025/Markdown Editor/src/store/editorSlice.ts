import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface EditorState {
  content: string;
  lastSaved: number;
  isDirty: boolean;
}

const initialState: EditorState = {
  content: '',
  lastSaved: Date.now(),
  isDirty: false,
};

export const editorSlice = createSlice({
  name: 'editor',
  initialState,
  reducers: {
    updateContent: (state, action: PayloadAction<string>) => {
      state.content = action.payload;
      state.isDirty = true;
    },
    markSaved: (state) => {
      state.lastSaved = Date.now();
      state.isDirty = false;
    },
  },
});

export const { updateContent, markSaved } = editorSlice.actions;
export default editorSlice.reducer;
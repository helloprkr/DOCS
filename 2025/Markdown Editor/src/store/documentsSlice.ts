import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { Document, saveDocument, getAllDocuments, deleteDocument } from '@/lib/storage';
import { nanoid } from '@reduxjs/toolkit';

interface DocumentsState {
  documents: Document[];
  activeDocumentId: string | null;
  loading: boolean;
  error: string | null;
}

const initialState: DocumentsState = {
  documents: [],
  activeDocumentId: null,
  loading: false,
  error: null,
};

export const fetchDocuments = createAsyncThunk(
  'documents/fetchAll',
  async () => {
    return getAllDocuments();
  }
);

export const createDocument = createAsyncThunk(
  'documents/create',
  async (title: string) => {
    const doc: Document = {
      id: nanoid(),
      title,
      content: '',
      lastModified: Date.now(),
      tags: [],
    };
    await saveDocument(doc);
    return doc;
  }
);

export const documentsSlice = createSlice({
  name: 'documents',
  initialState,
  reducers: {
    setActiveDocument: (state, action: PayloadAction<string>) => {
      state.activeDocumentId = action.payload;
    },
    updateDocument: (state, action: PayloadAction<Partial<Document>>) => {
      const index = state.documents.findIndex(doc => doc.id === state.activeDocumentId);
      if (index !== -1) {
        state.documents[index] = {
          ...state.documents[index],
          ...action.payload,
          lastModified: Date.now(),
        };
      }
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchDocuments.pending, (state) => {
        state.loading = true;
      })
      .addCase(fetchDocuments.fulfilled, (state, action) => {
        state.loading = false;
        state.documents = action.payload;
      })
      .addCase(fetchDocuments.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch documents';
      })
      .addCase(createDocument.fulfilled, (state, action) => {
        state.documents.unshift(action.payload);
        state.activeDocumentId = action.payload.id;
      });
  },
});

export const { setActiveDocument, updateDocument } = documentsSlice.actions;
export default documentsSlice.reducer;
import { get, set, del, entries } from 'idb-keyval';

export interface Document {
  id: string;
  title: string;
  content: string;
  lastModified: number;
  tags: string[];
}

const STORAGE_PREFIX = 'md-editor:';

export async function saveDocument(doc: Document): Promise<void> {
  await set(`${STORAGE_PREFIX}${doc.id}`, doc);
}

export async function getDocument(id: string): Promise<Document | null> {
  return get(`${STORAGE_PREFIX}${id}`);
}

export async function getAllDocuments(): Promise<Document[]> {
  const allEntries = await entries();
  return allEntries
    .filter(([key]) => key.toString().startsWith(STORAGE_PREFIX))
    .map(([_, value]) => value as Document)
    .sort((a, b) => b.lastModified - a.lastModified);
}

export async function deleteDocument(id: string): Promise<void> {
  await del(`${STORAGE_PREFIX}${id}`);
}
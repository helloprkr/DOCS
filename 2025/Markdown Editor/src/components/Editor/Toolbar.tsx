import { Button } from '@/components/ui/button';
import { Save, Download, Upload } from 'lucide-react';
import { useSelector } from 'react-redux';
import { RootState } from '@/store/store';
import { calculateStats } from '@/lib/markdown';

export function Toolbar() {
  const content = useSelector((state: RootState) => state.editor.content);
  const stats = calculateStats(content);

  return (
    <div className="border-b p-2 flex items-center justify-between">
      <div className="flex items-center gap-2">
        <Button variant="ghost" size="sm">
          <Save className="h-4 w-4 mr-2" />
          Save
        </Button>
        <Button variant="ghost" size="sm">
          <Download className="h-4 w-4 mr-2" />
          Export
        </Button>
        <Button variant="ghost" size="sm">
          <Upload className="h-4 w-4 mr-2" />
          Import
        </Button>
      </div>
      
      <div className="flex items-center gap-4 text-sm text-muted-foreground">
        <span>{stats.words} words</span>
        <span>{stats.readingTime} min read</span>
        <span>{stats.lines} lines</span>
      </div>
    </div>
  );
}
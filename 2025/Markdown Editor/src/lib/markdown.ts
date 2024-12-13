import { marked } from 'marked';
import Prism from 'prismjs';
import 'prismjs/components/prism-markdown';
import 'prismjs/components/prism-latex';
import 'prismjs/components/prism-mermaid';

// Configure marked with custom extensions
marked.use({
  renderer: {
    code(code, language) {
      if (language) {
        const highlighted = Prism.highlight(
          code,
          Prism.languages[language] || Prism.languages.text,
          language
        );
        return `<pre><code class="language-${language}">${highlighted}</code></pre>`;
      }
      return `<pre><code>${code}</code></pre>`;
    },
  },
  extensions: [{
    name: 'task',
    level: 'inline',
    start(src: string) {
      return src.match(/\[@\w+\]/)?.index;
    },
    tokenizer(src: string) {
      const rule = /^\[@(\w+)\]\s*(.+?)(?:\{([^}]+)\})?/;
      const match = rule.exec(src);
      if (match) {
        return {
          type: 'task',
          raw: match[0],
          priority: match[1],
          text: match[2],
          date: match[3],
        };
      }
    },
    renderer(token: any) {
      return `<span class="task task-${token.priority.toLowerCase()}">${token.text}${
        token.date ? ` (Due: ${token.date})` : ''
      }</span>`;
    },
  }],
});

export function parseMarkdown(content: string): string {
  return marked(content);
}

export function calculateStats(content: string) {
  const words = content.trim().split(/\s+/).length;
  const readingTime = Math.ceil(words / 200); // Assuming 200 words per minute
  
  return {
    words,
    readingTime,
    characters: content.length,
    lines: content.split('\n').length,
  };
}
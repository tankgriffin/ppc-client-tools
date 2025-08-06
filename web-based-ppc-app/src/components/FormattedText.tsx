import React from 'react';

interface FormattedTextProps {
  text: string;
  className?: string;
}

export function FormattedText({ text, className = '' }: FormattedTextProps) {
  if (!text || text.trim().length === 0) {
    return <p className="text-gray-500 italic">No content available</p>;
  }

  const formatText = (rawText: string) => {
    const lines = rawText.split('\n');
    const elements: JSX.Element[] = [];
    let currentList: string[] = [];
    let inCodeBlock = false;
    let codeBlockContent: string[] = [];

    const flushCurrentList = () => {
      if (currentList.length > 0) {
        elements.push(
          <ul key={`list-${elements.length}`} className="space-y-3 my-6 ml-6 bg-gray-50 p-4 rounded-lg border-l-4 border-blue-400">
            {currentList.map((item, index) => (
              <li key={index} className="text-gray-800 leading-relaxed flex items-start">
                <span className="text-blue-600 font-bold text-lg mr-3 mt-0.5">•</span>
                <span className="flex-1">{formatInlineText(item)}</span>
              </li>
            ))}
          </ul>
        );
        currentList = [];
      }
    };

    const flushCodeBlock = () => {
      if (codeBlockContent.length > 0) {
        elements.push(
          <pre key={`code-${elements.length}`} className="bg-gray-100 border border-gray-300 rounded-lg p-4 my-4 overflow-x-auto">
            <code className="text-sm text-gray-800 font-mono">
              {codeBlockContent.join('\n')}
            </code>
          </pre>
        );
        codeBlockContent = [];
      }
    };

    lines.forEach((line, index) => {
      const trimmedLine = line.trim();

      // Skip empty lines entirely
      if (trimmedLine.length === 0) {
        return;
      }

      // Handle code blocks
      if (trimmedLine.startsWith('```')) {
        if (inCodeBlock) {
          flushCodeBlock();
          inCodeBlock = false;
        } else {
          flushCurrentList();
          inCodeBlock = true;
        }
        return;
      }

      if (inCodeBlock) {
        codeBlockContent.push(line);
        return;
      }

      // Handle horizontal rules (---)
      if (trimmedLine.match(/^-{3,}$/)) {
        flushCurrentList();
        elements.push(
          <hr key={`hr-${index}`} className="my-8 border-gray-300" />
        );
        return;
      }

      // Handle H1 headings (# Title)
      if (trimmedLine.match(/^#\s+(.+)/)) {
        flushCurrentList();
        const title = trimmedLine.replace(/^#\s+/, '');
        elements.push(
          <h1 key={`h1-${index}`} className="text-4xl font-black text-blue-900 mt-10 mb-8 pb-4 border-b-4 border-blue-300 bg-blue-50 px-4 py-3 rounded-lg">
            {formatInlineText(title)}
          </h1>
        );
        return;
      }

      // Handle H2 headings (## Title)
      if (trimmedLine.match(/^##\s+(.+)/)) {
        flushCurrentList();
        const title = trimmedLine.replace(/^##\s+/, '');
        elements.push(
          <h2 key={`h2-${index}`} className="text-3xl font-bold text-gray-900 mt-8 mb-6 pb-3 border-b-2 border-gray-400 bg-gray-50 px-3 py-2 rounded">
            {formatInlineText(title)}
          </h2>
        );
        return;
      }

      // Handle H3 headings (### Title)
      if (trimmedLine.match(/^###\s+(.+)/)) {
        flushCurrentList();
        const title = trimmedLine.replace(/^###\s+/, '');
        elements.push(
          <h3 key={`h3-${index}`} className="text-2xl font-bold text-green-800 mt-6 mb-4 px-2 py-1 bg-green-50 border-l-4 border-green-500">
            {formatInlineText(title)}
          </h3>
        );
        return;
      }

      // Handle H4 headings (#### Title)
      if (trimmedLine.match(/^####\s+(.+)/)) {
        flushCurrentList();
        const title = trimmedLine.replace(/^####\s+/, '');
        elements.push(
          <h4 key={`h4-${index}`} className="text-xl font-bold text-purple-700 mt-5 mb-3 px-2 py-1 bg-purple-50 border-l-2 border-purple-400">
            {formatInlineText(title)}
          </h4>
        );
        return;
      }

      // Handle bullet points (- item)
      if (trimmedLine.match(/^-\s+(.+)/)) {
        const content = trimmedLine.replace(/^-\s+/, '');
        currentList.push(content);
        return;
      }

      // Handle numbered sections like "## 1. Market Position Assessment"
      if (trimmedLine.match(/^##\s+\d+\.\s+(.+)/)) {
        flushCurrentList();
        const title = trimmedLine.replace(/^##\s+/, '');
        elements.push(
          <h2 key={`numbered-h2-${index}`} className="text-3xl font-bold text-white bg-blue-700 mt-10 mb-6 py-4 px-6 rounded-lg flex items-center shadow-lg">
            <span className="w-12 h-12 bg-white text-blue-700 rounded-full text-xl font-black flex items-center justify-center mr-6">
              {trimmedLine.match(/\d+/)?.[0]}
            </span>
            {formatInlineText(title.replace(/^\d+\.\s+/, ''))}
          </h2>
        );
        return;
      }

      // Handle sections with bold patterns like "**Phase 1 (Months 1-2): Foundation Building - $500/month**"
      if (trimmedLine.match(/^\*\*(.+?)\*\*/)) {
        flushCurrentList();
        const title = trimmedLine.replace(/^\*\*(.+?)\*\*.*/, '$1');
        const rest = trimmedLine.replace(/^\*\*(.+?)\*\*(.*)/, '$2').trim();
        elements.push(
          <div key={`bold-section-${index}`} className="bg-yellow-100 border-l-4 border-yellow-500 p-4 my-4 rounded-r-lg">
            <h4 className="text-xl font-bold text-yellow-800">
              {title}
              {rest && <span className="font-medium text-yellow-700 ml-2">{rest}</span>}
            </h4>
          </div>
        );
        return;
      }

      // Handle regular paragraphs
      if (trimmedLine.length > 0) {
        flushCurrentList();
        
        // Check if it's a descriptive line (like "Core Demographics:" followed by list items)
        if (trimmedLine.endsWith(':') && trimmedLine.length < 50) {
          elements.push(
            <h5 key={`desc-${index}`} className="text-lg font-bold text-orange-700 mt-6 mb-3 bg-orange-50 px-3 py-2 rounded border-l-4 border-orange-400">
              {formatInlineText(trimmedLine)}
            </h5>
          );
          return;
        }

        elements.push(
          <p key={`p-${index}`} className="text-gray-800 leading-relaxed my-4 text-base pl-2">
            {formatInlineText(trimmedLine)}
          </p>
        );
      }
    });

    // Flush any remaining content
    flushCurrentList();
    flushCodeBlock();

    return elements;
  };

  const formatInlineText = (text: string) => {
    // Handle bold text (**text**)
    let formatted = text.replace(/\*\*([^*]+)\*\*/g, '<strong class="font-black text-blue-900 bg-blue-50 px-1 py-0.5 rounded">$1</strong>');
    
    // Handle italic text (*text*)
    formatted = formatted.replace(/\*([^*]+)\*/g, '<em class="italic font-medium text-purple-700">$1</em>');
    
    // Handle inline code (`code`)
    formatted = formatted.replace(/`([^`]+)`/g, '<code class="bg-gray-800 text-white px-2 py-1 rounded text-sm font-mono font-bold">$1</code>');
    
    // Handle URLs
    formatted = formatted.replace(/(https?:\/\/[^\s]+)/g, '<a href="$1" target="_blank" rel="noopener noreferrer" class="text-blue-600 hover:text-blue-800 underline font-bold">$1</a>');
    
    return <span dangerouslySetInnerHTML={{ __html: formatted }} />;
  };

  const formattedElements = formatText(text);

  return (
    <div className={`prose max-w-none ${className}`}>
      {formattedElements.length > 0 ? formattedElements : (
        <p className="text-gray-500 italic">No formatted content available</p>
      )}
    </div>
  );
}
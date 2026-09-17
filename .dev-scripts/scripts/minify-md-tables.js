const fs = require('fs');
const path = require('path');

const files = [];
function walk(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.name === 'node_modules') continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      walk(full);
    } else if (entry.name.endsWith('.md')) {
      files.push(full);
    }
  }
}
walk('.');

function minifyLine(line) {
  const trimmed = line.trim();
  if (!trimmed.startsWith('|')) return line;

  const parts = trimmed.split('|');
  let cells;
  if (trimmed.startsWith('|') && trimmed.endsWith('|')) {
    cells = parts.slice(1, -1);
  } else if (trimmed.startsWith('|')) {
    cells = parts.slice(1);
  } else if (trimmed.endsWith('|')) {
    cells = parts.slice(0, -1);
  } else {
    cells = parts;
  }

  const isSep = cells.every((c) => /^[-:\s]*$/.test(c));
  if (isSep) {
    return '| ' + cells.map(() => '---').join(' | ') + ' |';
  }
  return '| ' + cells.map((c) => c.trim()).join(' | ') + ' |';
}

let changed = 0;
for (const file of files) {
  let content = fs.readFileSync(file, 'utf8');
  const lines = content.split('\n');
  const result = [];
  let inCodeBlock = false;
  let tableLines = [];

  function flushTable() {
    if (tableLines.length === 0) return;
    for (const line of tableLines) {
      result.push(minifyLine(line));
    }
    tableLines = [];
  }

  for (const line of lines) {
    const trimmed = line.trim();
    if (trimmed.startsWith('```')) {
      flushTable();
      inCodeBlock = !inCodeBlock;
      result.push(line);
      continue;
    }
    if (inCodeBlock) {
      flushTable();
      result.push(line);
      continue;
    }
    if (trimmed.startsWith('|')) {
      tableLines.push(line);
    } else {
      flushTable();
      result.push(line);
    }
  }
  flushTable();

  const newContent = result.join('\n');
  if (newContent !== content) {
    fs.writeFileSync(file, newContent);
    changed++;
  }
}

console.log(`Minified tables in ${changed} files`);

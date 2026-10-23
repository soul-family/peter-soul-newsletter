const fs = require('fs');
const path = require('path');

const targetFiles = process.argv.slice(2);

function parseCells(line) {
  const trimmed = line.trim();
  if (!trimmed.startsWith('|')) return null;
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
  return cells.map((c) => c.trim());
}

function minifyLine(line, expectedCols) {
  const cells = parseCells(line);
  if (!cells) return line;

  const isSep = cells.every((c) => /^[-:\s]*$/.test(c));
  if (isSep) {
    const cols = expectedCols || cells.length;
    return '| ' + Array(cols).fill('---').join(' | ') + ' |';
  }

  if (expectedCols && cells.length > expectedCols) {
    const splitRows = [];
    let current = [];
    for (const cell of cells) {
      current.push(cell);
      if (cell === '' && current.length > 1) {
        const candidate = current.slice(0, -1);
        if (candidate.length <= expectedCols) {
          splitRows.push(candidate);
          current = [];
        }
      }
    }
    if (current.length > 0) splitRows.push(current);

    return splitRows
      .map((row) => {
        while (row.length < expectedCols) row.push('');
        return '| ' + row.join(' | ') + ' |';
      })
      .join('\n');
  }

  if (expectedCols && cells.length < expectedCols) {
    while (cells.length < expectedCols) cells.push('');
  }
  return '| ' + cells.join(' | ') + ' |';
}

function processFile(filePath) {
  let content = fs.readFileSync(filePath, 'utf8');
  const lines = content.split('\n');
  const result = [];
  let inCodeBlock = false;
  let tableLines = [];

  function flushTable() {
    if (tableLines.length === 0) return;
    let expectedCols = null;
    if (tableLines.length >= 2) {
      const headerCells = parseCells(tableLines[0]);
      const sepCells = parseCells(tableLines[1]);
      if (headerCells && sepCells) {
        expectedCols = headerCells.length;
      }
    }
    for (const line of tableLines) {
      const minified = minifyLine(line, expectedCols);
      if (minified.includes('\n')) {
        minified.split('\n').forEach((part) => result.push(part));
      } else {
        result.push(minified);
      }
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
    fs.writeFileSync(filePath, newContent);
    return true;
  }
  return false;
}

let changed = 0;
let filesProcessed = 0;

if (targetFiles.length > 0) {
  for (const file of targetFiles) {
    if (file.endsWith('.md')) {
      filesProcessed++;
      if (processFile(file)) {
        changed++;
        console.log(`Minified: ${file}`);
      }
    }
  }
} else {
  const root = process.cwd();
  function walk(dir) {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
      if (entry.name === 'node_modules') continue;
      const full = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        walk(full);
      } else if (entry.name.endsWith('.md')) {
        filesProcessed++;
        if (processFile(full)) {
          changed++;
          console.log(`Minified: ${path.relative(root, full)}`);
        }
      }
    }
  }
  walk(root);
}

console.log(`Minified tables in ${changed} of ${filesProcessed} markdown files`);

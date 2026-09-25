const fs = require('fs');
const path = require('path');

const srcContent = path.join(__dirname, '..', '..', 'src-content');

function removeLayoutMeta(filePath) {
  let content = fs.readFileSync(filePath, 'utf8');
  const original = content;

  content = content.replace(/^layout:.*(?:\r?\n)/gm, '');

  if (content !== original) {
    fs.writeFileSync(filePath, content, 'utf8');
    console.log(`Removed layout: ${path.relative(srcContent, filePath)}`);
  }
}

function walk(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.name.startsWith('_')) continue;
    if (entry.isDirectory()) walk(full);
    else if (entry.name.endsWith('.md')) removeLayoutMeta(full);
  }
}

walk(srcContent);
console.log('Done');

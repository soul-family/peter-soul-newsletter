const fs = require('fs');
const path = require('path');

const srcContent = path.join(__dirname, '..', '..', 'src-content');

function updateFile(filePath) {
  let content = fs.readFileSync(filePath, 'utf8');
  const original = content;
  let changed = false;

  content = content.replace(/^body_class:.*(?:\r?\n)/gm, (match) => {
    changed = true;
    return match.replace('body_class', 'background');
  });

  content = content.replace(/^permalink:.*(?:\r?\n)?/gm, (match) => {
    changed = true;
    return '';
  });

  if (changed) {
    fs.writeFileSync(filePath, content, 'utf8');
    console.log(`Updated: ${path.relative(srcContent, filePath)}`);
  }
}

function walk(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.name.startsWith('_')) continue;
    if (entry.isDirectory()) walk(full);
    else if (entry.name.endsWith('.md')) updateFile(full);
  }
}

walk(srcContent);
console.log('Done');

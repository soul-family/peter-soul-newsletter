const fs = require('fs');
const path = require('path');

const srcContent = path.join(__dirname, '..', '..', 'src-content');

const monthMap = {
  january: '01',
  february: '02',
  march: '03',
  april: '04',
  may: '05',
  june: '06',
  july: '07',
  august: '08',
  september: '09',
  october: '10',
  november: '11',
  december: '12',
};

function updateDate(filePath) {
  let content = fs.readFileSync(filePath, 'utf8');
  const original = content;

  content = content.replace(
    /^(\s*date:\s*)'([A-Za-z]+)\s+(\d{4})'(\s*\r?\n)/m,
    (match, prefix, monthName, year, suffix) => {
      const monthNum = monthMap[monthName.toLowerCase()];
      if (monthNum) {
        return `${prefix}'${year}/${monthNum}'${suffix}`;
      }
      return match;
    }
  );

  if (content !== original) {
    fs.writeFileSync(filePath, content, 'utf8');
    console.log(`Updated: ${path.relative(srcContent, filePath)}`);
  }
}

function walk(dir) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.name.startsWith('_')) continue;
    if (entry.isDirectory()) walk(full);
    else if (entry.name.endsWith('.md')) updateDate(full);
  }
}

walk(srcContent);
console.log('Done');

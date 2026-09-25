const fs = require('fs');
const path = require('path');

const columnsIndex = path.join(__dirname, '..', '..', 'src-content', 'content', 'columns', 'index.md');

const monthMap = {
  'january': 'January', 'february': 'February', 'march': 'March', 'april': 'April',
  'may': 'May', 'june': 'June', 'july': 'July', 'august': 'August',
  'september': 'September', 'october': 'October', 'november': 'November', 'december': 'December'
};

let content = fs.readFileSync(columnsIndex, 'utf8');
const lines = content.split('\n');
const updatedLines = lines.map(line => {
  const match = line.match(/^- (\w+) (\d{4}) - \[([^\]]+)\]\(([^)]+)\)$/);
  if (match) {
    const monthName = match[1].toLowerCase();
    const year = match[2];
    const title = match[3];
    const link = match[4];
    const monthText = monthMap[monthName] || match[1];
    return `- ${year} ${monthText} - [${title}](${link})`;
  }
  return line;
});

fs.writeFileSync(columnsIndex, updatedLines.join('\n'), 'utf8');
console.log('Updated columns index format');

from pathlib import Path
p = Path('src-content/content/columns/2003/2003-05-tyres-and-mileages.html')
text = p.read_text(encoding='utf-8')
lines = text.split('\n')
print('First 5 lines:')
for i, line in enumerate(lines[:5], 1):
    print(f'{i}: {repr(line)}')
print()
print('Has <!doctype html>:', '<!doctype html>' in text)
print('Has <html>:', '<html>' in text and '<HTML>' not in text)
print('Has <head>:', '<head>' in text and '<HEAD>' not in text)
print('Has <meta charset>:', '<meta charset' in text)
print('Has <img:', '<img' in text)
print('Has <IMG:', '<IMG' in text)

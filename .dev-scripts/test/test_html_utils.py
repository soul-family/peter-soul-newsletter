import unittest
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from shared.html_utils import (
    is_blog_post,
    transform_link,
    fix_hrefs,
    check_href_issues,
    verify_links,
)


class TestHtmlUtils(unittest.TestCase):
    def test_is_blog_post(self):
        assert is_blog_post('july_2002.html') is True
        assert is_blog_post('september_2002.html') is True
        assert is_blog_post('january_2019.html') is True
        assert is_blog_post('escaping.html') is False
        assert is_blog_post('contact.html') is False
        assert is_blog_post('info.html') is False
        assert is_blog_post('links.html') is False
        assert is_blog_post('letters.html') is False
        assert is_blog_post('familytree.html') is False

    def test_transform_link_columns_page(self):
        blog_posts = {'july_2002.html', 'september_2002.html'}
        assert transform_link('../html/links.html', True, blog_posts) == './'
        assert transform_link('../html\\links.html', True, blog_posts) == './'
        assert transform_link('../html/links.html#2019', True, blog_posts) == './#2019'
        assert transform_link('../html/info.html', True, blog_posts) == '../info.html'
        assert transform_link('../html/escaping.html', True, blog_posts) == '../escaping.html'
        assert transform_link('../html/july_2002.html', True, blog_posts) == 'july_2002.html'
        assert transform_link('../html/september_2002.html', True, blog_posts) == 'september_2002.html'

    def test_transform_link_main_index(self):
        blog_posts = {'july_2002.html', 'september_2002.html'}
        assert transform_link('./html/links.html', False, blog_posts) == './columns/'
        assert transform_link('./html\\links.html', False, blog_posts) == './columns/'
        assert transform_link('./html/links.html#2019', False, blog_posts) == './columns/#2019'
        assert transform_link('./html/info.html', False, blog_posts) == './info.html'
        assert transform_link('./html/escaping.html', False, blog_posts) == './escaping.html'
        assert transform_link('./html/contact.html', False, blog_posts) == './contact.html'
        assert transform_link('./html/july_2002.html', False, blog_posts) == './columns/july_2002.html'
        assert transform_link('./html/september_2002.html', False, blog_posts) == './columns/september_2002.html'

    def test_transform_link_passthrough(self):
        blog_posts = set()
        assert transform_link('./index.html', False, blog_posts) == './index.html'
        assert transform_link('../index.html', True, blog_posts) == '../index.html'
        assert transform_link('http://example.com', False, blog_posts) == 'http://example.com'

    def test_verify_links(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            base = Path(tmpdir)
            html = '<A HREF="./exists.html">link</A> <A HREF="./missing.html">missing</A>'
            (base / 'exists.html').write_text('ok')
            issues = verify_links(html, base)
            assert len(issues) == 1
            assert 'missing.html' in issues[0]

    def test_fix_hrefs_batch(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            preps = Path(tmpdir) / 'src-preps'
            preps.mkdir()
            cols = preps / 'commit1' / 'src-content' / 'content' / 'columns'
            cols.mkdir(parents=True)
            f = cols / 'july_2002.html'
            f.write_bytes(b'<A HREF="../links.html">Links</A>')
            
            fixed, errors = fix_hrefs(preps)
            assert fixed == 1
            assert errors == 0
            assert b'../columns/' in f.read_bytes()

    def test_check_href_issues_detects_broken(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            preps = Path(tmpdir) / 'src-preps'
            preps.mkdir()
            cols = preps / 'commit1' / 'src-content' / 'content' / 'columns'
            cols.mkdir(parents=True)
            f = cols / 'july_2002.html'
            f.write_bytes(b'<A HREF="../html/links.html">Links</A>')
            
            issues = check_href_issues(preps)
            assert len(issues) == 1
            assert '../html/links.html' in issues[0][1]


if __name__ == '__main__':
    unittest.main()

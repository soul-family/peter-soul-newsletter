#!/usr/bin/env python3
"""
test_link_utils.py — tests for shared link transformation utilities.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / '.dev-scripts' / 'shared'))

from link_utils import is_blog_post, transform_link, verify_links

def test_is_blog_post():
    assert is_blog_post('july_2002.html') is True
    assert is_blog_post('september_2002.html') is True
    assert is_blog_post('january_2019.html') is True
    assert is_blog_post('escaping.html') is False
    assert is_blog_post('contact.html') is False
    assert is_blog_post('info.html') is False
    assert is_blog_post('links.html') is False
    assert is_blog_post('letters.html') is False
    assert is_blog_post('familytree.html') is False
    assert is_blog_post('baileyfamilytree.html') is False
    print('test_is_blog_post: PASSED')

def test_transform_link_columns_page():
    blog_posts = {'july_2002.html', 'september_2002.html'}
    
    assert transform_link('../html/links.html', True, blog_posts) == './'
    assert transform_link('../html\\links.html', True, blog_posts) == './'
    assert transform_link('../html/links.html#2019', True, blog_posts) == './#2019'
    assert transform_link('../html/info.html', True, blog_posts) == '../info.html'
    assert transform_link('../html/escaping.html', True, blog_posts) == '../escaping.html'
    assert transform_link('../html/july_2002.html', True, blog_posts) == 'july_2002.html'
    assert transform_link('../html/september_2002.html', True, blog_posts) == 'september_2002.html'
    
    print('test_transform_link_columns_page: PASSED')

def test_transform_link_main_index():
    blog_posts = {'july_2002.html', 'september_2002.html'}
    
    assert transform_link('./html/links.html', False, blog_posts) == './columns/'
    assert transform_link('./html\\links.html', False, blog_posts) == './columns/'
    assert transform_link('./html/links.html#2019', False, blog_posts) == './columns/#2019'
    assert transform_link('./html/info.html', False, blog_posts) == './info.html'
    assert transform_link('./html/escaping.html', False, blog_posts) == './escaping.html'
    assert transform_link('./html/contact.html', False, blog_posts) == './contact.html'
    assert transform_link('./html/july_2002.html', False, blog_posts) == './columns/july_2002.html'
    assert transform_link('./html/september_2002.html', False, blog_posts) == './columns/september_2002.html'
    
    print('test_transform_link_main_index: PASSED')

def test_transform_link_passthrough():
    blog_posts = set()
    assert transform_link('./index.html', False, blog_posts) == './index.html'
    assert transform_link('../index.html', True, blog_posts) == '../index.html'
    assert transform_link('http://example.com', False, blog_posts) == 'http://example.com'
    
    print('test_transform_link_passthrough: PASSED')

def test_verify_links():
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        base = Path(tmpdir)
        html = '<A HREF="./exists.html">link</A> <A HREF="./missing.html">missing</A>'
        (base / 'exists.html').write_text('ok')
        issues = verify_links(html, base)
        assert len(issues) == 1
        assert 'missing.html' in issues[0]
    
    print('test_verify_links: PASSED')

if __name__ == '__main__':
    test_is_blog_post()
    test_transform_link_columns_page()
    test_transform_link_main_index()
    test_transform_link_passthrough()
    test_verify_links()
    print('\nAll tests passed.')

"""Helper for scripts that read book-of-mormon-1830.md: remove its YAML frontmatter."""


def strip_frontmatter(t):
    """Remove the YAML frontmatter block that compile_markdown.py puts at the top of book-of-mormon-1830.md."""
    if t.startswith('---\n'):
        end = t.find('\n---\n', 4)
        if end != -1:
            return t[end + 5:].lstrip('\n')
    return t


REPO = 'https://github.com/lds-restoration-documents/1830-grandin-palmyra-book-of-mormon'


def txt_header(sparse=False):
    """One-line header put at the top of the .txt outputs."""
    return f"# The Book of Mormon (Palmyra, 1830, E. B. Grandin; {'sparse, ' if sparse else ''}AI draft, no full human proofread) - {REPO}\n\n"

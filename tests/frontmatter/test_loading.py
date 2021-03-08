import io
import textwrap

import pytest
import yaml

import frontmatter as _frontmatter

standard_line_break = "\n"
normalize_line = f"{{}}{standard_line_break}".format


@pytest.fixture(
    params=[
        "\r\n",
        standard_line_break,
    ]
)
def line_break(request):
    return request.param


@pytest.fixture(
    params=[
        ["Hello, world"],
        ["Hello, world!", "---"],
    ]
)
def content(request, line_break):
    lines = request.param

    return line_break.join(lines)


@pytest.mark.parametrize(
    "separator",
    [
        "...",
        "---",
    ],
)
def test_should_load_frontmatter(content, separator, line_break):
    metadata = {"metadata": "Test", "value": True}
    frontmatter = yaml.dump(
        metadata,
        Dumper=yaml.SafeDumper,
        line_break=line_break,
        explicit_start=True,
    )
    document = f"{frontmatter}{separator}{line_break}{content}"

    document = _frontmatter.loads(document)

    assert document.metadata == metadata
    assert document.content == "".join(map(normalize_line, content.splitlines()))


def test_should_return_none_for_frontmatter_when_none_is_present(content):
    document = _frontmatter.loads(content)

    assert document.metadata == {}
    assert document.content == "".join(map(normalize_line, content.splitlines()))


def test_loading_from_file_should_work_with_weird_newlines():
    input_lines = "a\nb\r\nc\n"
    fp = io.StringIO(input_lines)
    document = _frontmatter.load(fp)

    assert document.content == "".join(map(normalize_line, input_lines.splitlines()))


@pytest.mark.parametrize(
    "input_document",
    [
        "",
        "---",
        "---\n",
        "\n",
    ],
)
def test_loads_empty_document(input_document):
    document = _frontmatter.load("")

    assert document.frontmatter is None, "Frontmatter should be None"
    assert document.metadata == {}, "Metadata should be empty"
    assert document.content == standard_line_break, "Content should be an empty line"


def test_convience_document_getter():
    content = textwrap.dedent(
        """\
            ---
            num: 123
            str: test
            ---
        """
    )
    document = _frontmatter.loads(content)
    assert document["num"] == 123
    assert document["str"] == "test"


def test_convience_document_setter():
    document = _frontmatter.loads("")
    assert document.metadata == {}
    document["test"] = "value"
    assert document.metadata == {"test": "value"}

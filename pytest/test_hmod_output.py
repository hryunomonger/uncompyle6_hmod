from io import StringIO

from xdis.cross_types import UnicodeForPython3

import uncompyle6.main as main_module
from uncompyle6.semantics.n_actions import NonterminalActions
from uncompyle6.util import better_repr


class _FakeNode(object):
    def __init__(self, attr=None, pattr=None):
        self.attr = attr
        self.pattr = pattr


class _FakeWriter(object):
    FUTURE_UNICODE_LITERALS = False
    version = (2, 7)

    def __init__(self):
        self.parts = []

    def write(self, value):
        self.parts.append(value)

    def pp_tuple(self, value):
        self.parts.append(repr(value))

    def prune(self):
        return None

    @property
    def text(self):
        return "".join(self.parts)


def test_better_repr_escapes_unicode_control_chars():
    value = UnicodeForPython3(bytes([2, 3, 9, 10, 13, 27, 31]))
    assert better_repr(value, (2, 7)) == "u'\\x02\\x03\\t\\n\\r\\x1b\\x1f'"


def test_better_repr_falls_back_to_bytes_for_invalid_utf8():
    value = UnicodeForPython3(b"\xed\xa0\x80")
    assert better_repr(value, (2, 7)) == "b'\\xed\\xa0\\x80'"


def test_better_repr_handles_nested_unicode_tuple_members():
    value = (UnicodeForPython3(b"\\"), UnicodeForPython3(b"'"))
    assert better_repr(value, (2, 7)) == "(u'\\\\', u'\\'')"


def test_n_load_const_handles_future_unicode_literals_without_invalid_bu_prefix():
    writer = _FakeWriter()
    writer.FUTURE_UNICODE_LITERALS = True
    node = _FakeNode(attr=UnicodeForPython3(b"template"), pattr=UnicodeForPython3(b"template"))
    NonterminalActions.n_LOAD_CONST(writer, node)
    assert writer.text == "b'template'"


def test_n_load_const_handles_unicode_for_python3_without_invalid_bu_prefix():
    writer = _FakeWriter()
    node = _FakeNode(attr=UnicodeForPython3(b"template"), pattr=UnicodeForPython3(b"template"))
    NonterminalActions.n_LOAD_CONST(writer, node)
    assert writer.text == "u'template'"


def test_decompile_file_preserves_partial_output_before_reraise(monkeypatch):
    def fake_check_object_path(filename):
        return filename

    def fake_load_module(filename, code_objects):
        return ((2, 7), None, None, object(), False, None, None)

    def fake_decompile(*args, **kwargs):
        args[2].write("def f():\n    return 1\n\nreturn\n")
        raise RuntimeError("boom")

    monkeypatch.setattr(main_module, "check_object_path", fake_check_object_path)
    monkeypatch.setattr(main_module, "load_module", fake_load_module)
    monkeypatch.setattr(main_module, "decompile", fake_decompile)

    out = StringIO()
    try:
        main_module.decompile_file("dummy.pyc", outstream=out)
    except RuntimeError as exc:
        assert str(exc) == "boom"
    else:
        raise AssertionError("RuntimeError was not raised")

    assert out.getvalue() == "def f():\n    return 1\n\n"

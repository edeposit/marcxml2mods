#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import os
import os.path
from lxml import etree
from lxml import isoschematron

import pytest

from marcxml2mods import transformators

from test_xslt_transformer import DIRNAME
from test_xslt_transformer import OAI_FILENAME


# Functions & classes =========================================================
def get_test_data_context(fn):
    return os.path.join(DIRNAME, fn)


def get_test_file_content(fn):
    fn = get_test_data_context(fn)

    with open(fn) as f:
        return f.read()


def validity_test(xml):
    xsd_doc = etree.parse(get_test_data_context("mods-3-4.xsd"))
    xsd = etree.XMLSchema(xsd_doc)
    xml = etree.fromstring(xml)
    result = xsd.validate(xml)

    if result == 0:
        raise ValueError(xsd.error_log.filter_from_errors()[0])


# Fixtures ====================================================================
@pytest.fixture
def post_mono_example():
    return get_test_file_content("postprocessed_mods.xml")


@pytest.fixture
def lang_example():
    return get_test_file_content("lang_example.oai")


@pytest.fixture
def post_lang_example():
    return get_test_file_content("postprocessed_lang_example.xml")


# Tests =======================================================================
def test_transform_to_mods_mono(post_mono_example):
    result = transformators.transform_to_mods_mono(
        OAI_FILENAME,
        "someid",
        "http://kitakitsune.org/raw",
    )

    assert result
    assert result[0] == post_mono_example

    validity_test(result[0])


def test_transform_to_mods_mono_lang_example(lang_example, post_lang_example):
    result = transformators.transform_to_mods_mono(
        lang_example,
        "someid",
        "http://kitakitsune.org/raw",
    )

    assert result
    assert result[0] == post_lang_example

    validity_test(result[0])


def test_marcxml2mods(post_mono_example):
    result = transformators.marcxml2mods(
        OAI_FILENAME,
        "someid",
        "http://kitakitsune.org/raw",
    )
    # TODO: Add tests for each type of document

    assert result
    assert result[0] == post_mono_example

    validity_test(result[0])

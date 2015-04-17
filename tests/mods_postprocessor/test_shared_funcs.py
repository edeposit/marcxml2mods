#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import pytest
import dhtmlparser

from marcxml2mods.mods_postprocessor import shared_funcs


# Fixtures ====================================================================
@pytest.fixture
def it_dom():
    return dhtmlparser.parseString("""
        <tag>
            <sometag />
            <othertag />
        </tag>
    """)


@pytest.fixture
def tc_dom():
    return dhtmlparser.parseString("""
        <tag>
            <sometag />
            <othertag>
                Somecontent.
            </othertag>
        </tag>
    """)


@pytest.fixture
def short_dom_str():
    return """
        <tag>
            <sometag />
            <othertag>Somecontent.</othertag>
        </tag>
    """


@pytest.fixture
def short_dom():
    return dhtmlparser.parseString(short_dom_str())


# Tests =======================================================================
def test_insert_tag(it_dom):
    dhtmlparser.makeDoubleLinked(it_dom)

    shared_funcs.insert_tag(
        tag=dhtmlparser.HTMLElement("<another />"),
        before=it_dom.find("othertag")[0],
        root=it_dom
    )

    assert it_dom.__str__() == """
        <tag>
            <sometag />
            <another /><othertag />
        </tag>
    """


def test_insert_tag_not_double_linked(it_dom):
    with pytest.raises(ValueError):
        shared_funcs.insert_tag(
            tag=dhtmlparser.HTMLElement("<another />"),
            before=it_dom.find("othertag")[0],
            root=it_dom
        )


def test_insert_tag_dont_use_before(it_dom):
    dhtmlparser.makeDoubleLinked(it_dom)

    shared_funcs.insert_tag(
        tag=dhtmlparser.HTMLElement("<another />"),
        before=None,
        root=it_dom.find("tag")[0]
    )

    assert it_dom.__str__() == """
        <tag>
            <sometag />
            <othertag />
        <another /></tag>
    """


def test_transform_content(tc_dom):
    shared_funcs.transform_content(
        tc_dom.find("othertag"),
        lambda x: x.getContent().strip()
    )

    assert tc_dom.__str__() == """
        <tag>
            <sometag />
            <othertag>Somecontent.</othertag>
        </tag>
    """


def test_transform_content_without_array(tc_dom):
    shared_funcs.transform_content(
        tc_dom.find("othertag")[0],
        lambda x: x.getContent().strip()
    )

    assert tc_dom.__str__() == """
        <tag>
            <sometag />
            <othertag>Somecontent.</othertag>
        </tag>
    """


def test_transform_content_numeric(short_dom):
    shared_funcs.transform_content(
        short_dom.find("othertag"),
        lambda x: str(len(x.getContent()))
    )

    assert short_dom.__str__() == """
        <tag>
            <sometag />
            <othertag>12</othertag>
        </tag>
    """


def test_double_linked_dom(short_dom):
    assert isinstance(short_dom, dhtmlparser.HTMLElement)
    dl_dom = shared_funcs.double_linked_dom(short_dom)
    assert isinstance(dl_dom, dhtmlparser.HTMLElement)

    assert hasattr(dl_dom.find("sometag")[0], "parent")
    assert dl_dom.find("sometag")[0].parent == dl_dom.find("tag")[0]


def test_double_linked_dom_from_str(short_dom_str):
    assert isinstance(short_dom_str, str)

    dl_dom = shared_funcs.double_linked_dom(short_dom_str)

    assert isinstance(dl_dom, dhtmlparser.HTMLElement)
    assert hasattr(dl_dom.find("sometag")[0], "parent")
    assert dl_dom.find("sometag")[0].parent == dl_dom.find("tag")[0]

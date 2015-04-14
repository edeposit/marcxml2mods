#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import os
import os.path

import dhtmlparser

import mods_postprocessor
from xslt_transformer import xslt_transformation


# Functions & classes =========================================================
def _template_path(fn):
    """
    Return Absolute path for filename from local ``xslt/`` directory.

    Args:
        fn (str): Filename. ``MARC21slim2MODS3-4-NDK.xsl`` for example.

    Returns:
        str: Absolute path to `fn` in ``xslt`` dicretory..
    """
    return os.path.join(os.path.dirname(__file__), "xslt", fn)


def _apply_postprocessing(xml, func, uuid):
    """
    Apply `func` to all ``<mods:mods>`` tags from `xml`. Insert UUID.

    Args:
        xml (str): XML which will be postprocessed.
        func (fn): Function, which will be used for postprocessing.
        uuid (str): UUID, which will be inserted to `xml`.

    Returns:
        list: List of string with postprocessed XML.
    """
    dom = dhtmlparser.parseString(xml)

    return [
        func(mods_tag, uuid, cnt)
        for cnt, mods_tag in enumerate(dom.find("mods:mods"))
    ]


def transform_to_mods_mono(marc_xml, uuid):
    """
    Convert `marc_xml` to MODS data format.

    Args:
        marc_xml (str): Filename or XML string. Don't use ``\\n`` in case of
                        filename.
        uuid (str): UUID string giving the package ID.

    Returns:
        list: Collection of transformed xml strings.
    """
    transformed = xslt_transformation(
        marc_xml,
        _template_path("MARC21slim2MODS3-4-NDK.xsl")
    )

    return _apply_postprocessing(
        xml=transformed,
        func=mods_postprocessor.postprocess_monograph,
        uuid=uuid
    )


def transform_to_mods_multimono(marc_xml, uuid):
    """
    Convert `marc_xml` to multimonograph MODS data format.

    Args:
        marc_xml (str): Filename or XML string. Don't use ``\\n`` in case of
                        filename.
        uuid (str): UUID string giving the package ID.

    Returns:
        list: Collection of transformed xml strings.
    """
    transformed = xslt_transformation(
        marc_xml,
        _template_path("MARC21toMultiMonographTitle.xsl")
    )

    return _apply_postprocessing(
        xml=transformed,
        func=mods_postprocessor.postprocess_monograph,  # TODO: multimono
        uuid=uuid
    )


def transform_to_mods_periodical(marc_xml, uuid):
    """
    Convert `marc_xml` to periodical MODS data format.

    Args:
        marc_xml (str): Filename or XML string. Don't use ``\\n`` in case of
                        filename.
        uuid (str): UUID string giving the package ID.

    Returns:
        str: Transformed xml as string.
    """
    transformed = xslt_transformation(
        marc_xml,
        _template_path("MARC21toPeriodicalTitle.xsl")
    )

    return _apply_postprocessing(
        xml=transformed,
        func=mods_postprocessor.postprocess_monograph,  # TODO: periodical
        uuid=uuid
    )


def marcxml2mods(marc_xml, uuid):
    pass

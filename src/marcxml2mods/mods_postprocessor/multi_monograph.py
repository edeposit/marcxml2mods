#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
import dhtmlparser

from monograph import add_uuid
from monograph import add_xml_declaration
from monograph import add_missing_xml_attributes


# Functions & classes =========================================================
@add_xml_declaration
def postprocess_multi_mono(mods, uuid, counter):
    # do not parse already parsed dom's
    dom = mods
    if not isinstance(mods, dhtmlparser.HTMLElement):
        dom = dhtmlparser.parseString(mods)
    dhtmlparser.makeDoubleLinked(dom)

    add_missing_xml_attributes(dom, counter)

    if uuid:
        add_uuid(dom, uuid)

    return dom.prettify()

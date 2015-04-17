#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from os.path import join
from os.path import dirname

import pytest
import dhtmlparser

from marcxml2mods import transformators
from marcxml2mods import xslt_transformer
from marcxml2mods.mods_postprocessor import monograph
from marcxml2mods.mods_postprocessor import shared_funcs


# Variables ===================================================================
DIRNAME = join(dirname(dirname(__file__)), "data")
OAI_FILENAME = join(DIRNAME, "oai_example.oai")


@pytest.fixture
def postprocessed():
    fn = join(DIRNAME, "postprocessed_mods.xml")

    with open(fn) as f:
        return f.read()


# Tests =======================================================================
def test_postprocess_mods_mono(postprocessed):
    result = transformators.transform_to_mods_mono(OAI_FILENAME, "someid")

    # with open("xex.xml", "wt") as f:
        # f.write(result[0])

    assert result[0] == postprocessed


def test_fix_location_tag():
    XML = """
<mods:mods>
  <mods:identifier type="ccnb">cnb000003024</mods:identifier>
  <mods:location>
    <mods:physicalLocation authority="siglaADR">ABA001</mods:physicalLocation>
    <mods:url displayLabel="electronic resource" usage="primary display">http://edeposit-test.nkp.cz/producents/beta-nakladatelstvi/epublications/controlling-v-msp-nejen-o-cislech/controlling.pdf</mods:url>
    <mods:url displayLabel="electronic resource">http://edeposit.nkp.cz/</mods:url>
  </mods:location>
  <mods:identifier type="uuid">236b6283-22d1-4014-ae50-a303cfd15419</mods:identifier>
  <mods:identifier type="isbn">978-80-7408-086-9</mods:identifier>
  <mods:relatedItem>
    <mods:location>
      <mods:url>http://edeposit.nkp.cz/</mods:url>
    </mods:location>
  </mods:relatedItem>
  <mods:identifier type="isbn">978-80-7408-086-9</mods:identifier>
</mods:mods>
    """
    dom = shared_funcs.double_linked_dom(XML)

    monograph.fix_location_tag(dom)

    assert dom.__str__() == """
<mods:mods>
  <mods:identifier type="ccnb">cnb000003024</mods:identifier>
  <mods:location>
    <mods:holdingSimple>
      <mods:copyInformation>
        <mods:electronicLocator>http://edeposit-test.nkp.cz/producents/beta-nakladatelstvi/epublications/controlling-v-msp-nejen-o-cislech/controlling.pdf</mods:electronicLocator>
      </mods:copyInformation>
    </mods:holdingSimple>
  </mods:location>
  <mods:identifier type="uuid">236b6283-22d1-4014-ae50-a303cfd15419</mods:identifier>
  <mods:identifier type="isbn">978-80-7408-086-9</mods:identifier>
  <mods:relatedItem>
    <mods:location>
      <mods:url>http://edeposit.nkp.cz/</mods:url>
    </mods:location>
  </mods:relatedItem>
  <mods:identifier type="isbn">978-80-7408-086-9</mods:identifier>
</mods:mods>
    """


def test_fix_related_item_tag():
    XML = """
<mods:mods>
  <mods:identifier type="ccnb">cnb000003024</mods:identifier>
  <mods:identifier type="uuid">236b6283-22d1-4014-ae50-a303cfd15419</mods:identifier>
  <mods:identifier type="isbn">978-80-7408-086-9</mods:identifier>
  <mods:relatedItem>
    <mods:location>
      <mods:url>http://edeposit.nkp.cz/</mods:url>
    </mods:location>
  </mods:relatedItem>
  <mods:identifier type="isbn">978-80-7408-086-9</mods:identifier>
</mods:mods>
    """
    dom = shared_funcs.double_linked_dom(XML)

    monograph.fix_related_item_tag(dom)

    assert dom.prettify() == """<mods:mods>
  <mods:identifier type="ccnb">cnb000003024</mods:identifier>
  <mods:identifier type="uuid">236b6283-22d1-4014-ae50-a303cfd15419</mods:identifier>
  <mods:identifier type="isbn">978-80-7408-086-9</mods:identifier>
    <mods:identifier type="isbn">978-80-7408-086-9</mods:identifier>
</mods:mods>
"""


def test_add_marccountry_tag():
    XML = """<mods:mods>
  <mods:originInfo>
    <mods:place>
      <mods:placeTerm type="text">Brno</mods:placeTerm>
    </mods:place>
  </mods:originInfo>
</mods:mods>
"""
    dom = shared_funcs.double_linked_dom(XML)

    monograph.add_marccountry_tag(dom)

    assert dom.prettify() == """<mods:mods>
  <mods:originInfo>
    <mods:place>
      <mods:placeTerm type="code" authority="marccountry">xr-</mods:placeTerm>
    </mods:place>
    <mods:place>
      <mods:placeTerm type="text">Brno</mods:placeTerm>
    </mods:place>
  </mods:originInfo>
</mods:mods>
"""
#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# Interpreter version: python 2.7
#
# Imports =====================================================================
from marcxml2mods import mods_postprocessor as mp


# Tests =======================================================================
def test_():
    assert mp.postprocess_monograph
    assert mp.postprocess_periodical
    assert mp.postprocess_multi_mono

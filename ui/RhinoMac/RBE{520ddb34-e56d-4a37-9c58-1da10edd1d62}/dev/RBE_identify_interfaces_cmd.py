from __future__ import print_function
from __future__ import absolute_import
from __future__ import division


import rhinoscriptsyntax as rs
import scriptcontext as sc

import Rhino

import os
import sys

import compas_rhino
import compas_rbe

from compas_rhino.utilities import XFunc

from compas_rbe.datastructures import Assembly


identify_interfaces_ = XFunc('compas_rbe.interfaces.identify_interfaces_xfunc', tmpdir=compas_rbe.TEMP)

identify_interfaces_.python = '/Users/vanmelet/anaconda3/bin/python3'
identify_interfaces_.paths = ['/Users/vanmelet/Code/BlockResearchGroup/compas_rbe/src']


def identify_interfaces(assembly, nmax=10, tmax=0.05, amin=0.01, lmin=0.01):
    data = {'assembly': assembly.to_data(),
            'blocks'  : {str(key): assembly.blocks[key].to_data() for key in assembly.blocks}}
    result = identify_interfaces_(data, nmax=nmax, tmax=tmax, amin=amin, lmin=lmin)
    assembly.data = result['assembly']
    for key in assembly.blocks:
        assembly.blocks[key].data = result['blocks'][str(key)]


__commandname__ = "RBE_identify_interfaces"


def RunCommand(is_interactive):
    if not 'RBE' in sc.sticky:
        raise Exception('Initialise RBE first!')

    RBE = sc.sticky['RBE']

    try:

        assembly = RBE['assembly']

        identify_interfaces(assembly)

        assembly.draw(RBE['settings']['layer'])

    except Exception as error:

        print(error)
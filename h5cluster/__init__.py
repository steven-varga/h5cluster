# -*- coding: utf-8 -*-
# ALL RIGHTS RESERVED.
# _____________________________________________________________________________
# NOTICE:   All  information  contained  herein is, and remains the property of
# Varga Consulting and  its suppliers, if  any. The intellectual and  technical
# concepts  contained  herein  are  proprietary  to  Varga Consulting  and  its
# suppliers and may be covered  by  Canadian  and  Foreign Patents, patents  in
# process, and are protected by trade secret or copyright law. Dissemination of
# this  information or reproduction of  this material is strictly forbidden un-
# less prior written permission is obtained from Varga Consulting.
#
# Copyright © <2019-2020> Varga Consulting, Toronto, ON info@vargaconsulting.ca
# _____________________________________________________________________________
import logging

"""Top-level package for cluster."""

__author__ = """Steven Varga"""
__email__ = 'steven@vargaconsulting.ca'
__version__ = '0.1.2'

logger = logging.getLogger(__name__)
logging.basicConfig(format='%(asctime)-10s %(levelname)-8s %(message)s',
                    datefmt='%H:%M:%S', level=logging.INFO)

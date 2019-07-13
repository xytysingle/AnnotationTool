#!/usr/bin/env python

import sys
sys.path.insert(0, '.')

from logger import setup_logging

logger = setup_logging(__name__)
logger.error('Test mail!')

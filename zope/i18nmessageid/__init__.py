##############################################################################
#
# Copyright (c) 2004 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""I18n Messages

$Id: __init__.py 30005 2005-04-15 16:17:58Z poster $
"""
# this is the old message id implementation; it is on the slate to be
# deprecated sometime in the future.
from messageid import MessageID, MessageIDFactory
# this is the new message id implementation.  It is the one to use if you
# have a choice.  Please see messages.txt for more details.
from message import Message, MessageFactory

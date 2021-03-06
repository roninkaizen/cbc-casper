"""The binary view module extends a view for binary data structures """
from casper.protocols.integer.integer_view import IntegerView


class BinaryView(IntegerView):
    """A view class that also keeps track of messages about a bit"""
    def __init__(self, messages=None, first_message=None):
        super().__init__(messages)


class MPTreeConversionError(Exception):
    def __init__(self, message, node):
        self.message = message
        self.node = node
        super().__init__(f"Error at node {node}: {message}")

class BadConversionError(MPTreeConversionError):
    """Exception for non-implemented"""
    def __init__(self, message, node):
        self.message = message
        self.node = node
        super().__init__(f"{message} not implemented: {node}", node)

class NotImplementedConversionError(MPTreeConversionError):
    """Exception for non-implemented"""
    def __init__(self, message, node):
        self.message = message
        self.node = node
        super().__init__(f"{message} not implemented: {node}", node)


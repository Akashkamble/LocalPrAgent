import structlog

def get_logger():
    """Returns a configured logger instance"""
    return structlog.get_logger()
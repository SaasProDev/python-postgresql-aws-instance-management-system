import asyncio
from concurrent.futures import _base

shutdown_exceptions = (GeneratorExit, _base.CancelledError, asyncio.CancelledError)

# http_exceptions = (Exception, )
# # ignored_exceptions = (Exception, )
# #
# # ContentTypeError = Exception
# # InvalidHeader = Exception
# # ContentEncodingError = Exception
# # LargeContentError = Exception
# # InvalidUrl = Exception
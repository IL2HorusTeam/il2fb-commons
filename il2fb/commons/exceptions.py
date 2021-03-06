from ._utils import export


@export
class IL2FBException(Exception):
  """Generic exception for 'il2fb' namespace."""


@export
class IL2FBLookupError(LookupError, IL2FBException):
  """Generic lookup error for 'il2fb' namespace."""


@export
class IL2FBParsingException(IL2FBException):
  """Generic parsing exception for 'il2fb' namespace."""

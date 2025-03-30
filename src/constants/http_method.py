from enum import Enum


class Method(Enum):
  """HTTP methods enumeration class.
  This class defines the HTTP methods used in the application.
  """
  GET = "GET"
  POST = "POST"
  PUT = "PUT"
  PATCH = "PATCH"
  DELETE = "DELETE"
  
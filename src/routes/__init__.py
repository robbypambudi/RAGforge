
from typing import List
from fastapi import FastAPI

from src.types.handler_request_type import HandlerRequestType


class RoutesRegister():
	"""
	Class to register routes
	"""
	def __init__(self, app: FastAPI):
		self.app = app

	def register_routes(self, routes: List[HandlerRequestType]):
		"""
		Register routes
		"""
		for route in routes:
			if route.method == "GET":
				self.app.get(route.path, status_code=route.status_code)(route.handler)
			elif route.method == "POST":
				self.app.post(route.path, status_code=route.status_code)(route.handler)
			elif route.method == "PUT":
				self.app.put(route.path, status_code=route.status_code)(route.handler)
			elif route.method == "DELETE":
				self.app.delete(route.path, status_code=route.status_code)(route.handler)
			elif route.method == "PATCH":
				self.app.patch(route.path, status_code=route.status_code)(route.handler)
			else:
				raise ValueError(f"Method {route.method} not supported")
		
	   
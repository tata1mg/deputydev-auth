from .auth import auth_route
from .service_health_checker import service_health_checker_route

__all_routes__ = [auth_route, service_health_checker_route]

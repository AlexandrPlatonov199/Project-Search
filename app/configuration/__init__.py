"""Collect or build all requirements for startup server.

In this module, you can add all your middlewares, routes, dependencies,
etc.

Containers need for register all dependencies in ``FastAPI`` server. For
start building your application, you **MUST** call wire_packages.

"""

from app.internal.services import Services
from app.pkg.connectors import Connectors, PostgresSQL
from app.pkg.models.core import Container, Containers
from app.pkg.models.core.containers import Resource

__all__ = ["__containers__"]


__containers__ = Containers(
    pkg_name=__name__,
    containers=[
        Container(container=Services),
        Resource(
            container=Connectors,
            depends_on=[Container(container=PostgresSQL)],
        ),
    ],
)
"""Models for dependency_injector containers."""

from dataclasses import dataclass, field
from typing import Callable, List, Optional, Type, Union

from dependency_injector import containers
from dependency_injector.containers import Container as _DIContainer
from fastapi import FastAPI

from app.pkg.models.core.meta import SingletonMeta

__all__ = ["Container", "Containers", "Resource"]


@dataclass(frozen=True)
class Resource:
    """Model for contain single resource.

    Attributes:
        container:
            dependency_injector resource container-callable object.
        depends_on:
            List of dependency_injector containers.
            Those containers MUST be wired to the main container.
            Default: []
        packages:
            Array of packages to which the injector will be available.
            Default: ["app"]
    """

    container: Type[_DIContainer]

    depends_on: List[containers.Container] = field(default_factory=list)

    packages: List[str] = field(default_factory=lambda: ["app"])


@dataclass(frozen=True)
class Container:
    """Model for contain single container.

    Attributes:
        container:
            dependency_injector declarative container callable object.
        packages:
            Array of packages to which the injector will be available.
            Default: ["app"]
    """

    container: Union[Callable[..., containers.Container]]

    packages: List[str] = field(default_factory=lambda: ["app"])


class WiredContainer(dict, metaclass=SingletonMeta):
    """Singleton container for store all wired containers."""

    def __getitem__(self, item: object):
        """Get container by name.

        Args:
            item: Container object.

        Returns:
            Container instance.
        """

        return super().__getitem__(item.__name__)


@dataclass(frozen=True)
class Containers:
    """Frozen dataclass model, for contains all declarative containers."""

    #: str: __name__ of the main package.
    pkg_name: str

    #: List[Container]: List of `Container` model.
    containers: List[Union[Container, Resource]]

    #: List[_Container]: List of instance dependency_injector containers.
    __wired_containers__: WiredContainer = field(
        init=False,
        default_factory=WiredContainer,
    )

    def wire_packages(
        self,
        app: Optional[FastAPI] = None,
        pkg_name: Optional[str] = None,
        unwire: bool = False,
    ):
        """Wire packages to the declarative containers.

        Args:
            app:
                Optional ``FastAPI`` instance.
                If passed, the containers will be written to the application context.
            pkg_name:
                Optional ``__name__`` of running module.
            unwire:
                Optional bool parameter. If `True`, un wiring all containers.

        Returns:
            None
        """
        pkg_name = pkg_name if pkg_name else self.pkg_name
        for container in self.containers:
            self.__wire(container, unwire, pkg_name, app)

            if not isinstance(container, Resource):
                continue

            for dep in container.depends_on:
                self.__wire(dep, unwire, pkg_name, app)

    def __wire(
        self,
        container: Union[Container, Resource],
        unwire: bool,
        pkg_name: str,
        app: Optional[FastAPI] = None,
    ) -> Container:
        """Wire container to the declarative containers.

        Args:
            container: Container or Resource model.
            unwire: Optional bool parameter. If `True`, un wiring all containers.
            pkg_name: Optional __name__ of running module.
            app: Optional ``FastAPI`` instance.
                if passed, the containers will be written to the application context.

        Returns:
            ``Container``
        """

        cont = container.container()

        if unwire:
            cont.unwire()
            return cont

        cont.wire(packages=[pkg_name, *container.packages])

        container_name = container.container.__name__

        if not self.__wired_containers__.get(container_name, None):
            self.__wired_containers__[container_name] = cont

        if app:
            setattr(app, container_name.lower(), cont)

        return cont

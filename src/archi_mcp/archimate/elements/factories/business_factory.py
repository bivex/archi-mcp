# Copyright (c) 2025 Bivex
#
# Author: Bivex
# Available for contact via email: support@b-b.top
# For up-to-date contact information:
# https://github.com/bivex
#
# Created: 2025-12-18T11:40:54
# Last Updated: 2025-12-18T11:40:54
#
# Licensed under the MIT License.
# Commercial licensing available upon request.

"""Factory for creating Business layer ArchiMate elements."""

from typing import Optional
from ..business import BusinessElement
from ..base import ArchiMateLayer, ArchiMateAspect


class BusinessElementFactory:
    """Factory class for creating Business layer elements."""

    @staticmethod
    def create_business_actor(
        id: str,
        name: str,
        description: Optional[str] = None,
        **kwargs
    ) -> BusinessElement:
        """Create a Business Actor element."""
        return BusinessElement(
            id=id,
            name=name,
            element_type="Actor",
            layer=ArchiMateLayer.BUSINESS,
            aspect=ArchiMateAspect.ACTIVE_STRUCTURE,
            description=description,
            **kwargs
        )

    @staticmethod
    def create_business_role(
        id: str,
        name: str,
        description: Optional[str] = None,
        **kwargs
    ) -> BusinessElement:
        """Create a Business Role element."""
        return BusinessElement(
            id=id,
            name=name,
            element_type="Role",
            layer=ArchiMateLayer.BUSINESS,
            aspect=ArchiMateAspect.ACTIVE_STRUCTURE,
            description=description,
            **kwargs
        )

    @staticmethod
    def create_business_collaboration(
        id: str,
        name: str,
        description: Optional[str] = None,
        **kwargs
    ) -> BusinessElement:
        """Create a Business Collaboration element."""
        return BusinessElement(
            id=id,
            name=name,
            element_type="Collaboration",
            layer=ArchiMateLayer.BUSINESS,
            aspect=ArchiMateAspect.ACTIVE_STRUCTURE,
            description=description,
            **kwargs
        )

    @staticmethod
    def create_business_interface(
        id: str,
        name: str,
        description: Optional[str] = None,
        **kwargs
    ) -> BusinessElement:
        """Create a Business Interface element."""
        return BusinessElement(
            id=id,
            name=name,
            element_type="Interface",
            layer=ArchiMateLayer.BUSINESS,
            aspect=ArchiMateAspect.ACTIVE_STRUCTURE,
            description=description,
            **kwargs
        )

    @staticmethod
    def create_business_process(
        id: str,
        name: str,
        description: Optional[str] = None,
        **kwargs
    ) -> BusinessElement:
        """Create a Business Process element."""
        return BusinessElement(
            id=id,
            name=name,
            element_type="Process",
            layer=ArchiMateLayer.BUSINESS,
            aspect=ArchiMateAspect.BEHAVIOR,
            description=description,
            **kwargs
        )

    @staticmethod
    def create_business_function(
        id: str,
        name: str,
        description: Optional[str] = None,
        **kwargs
    ) -> BusinessElement:
        """Create a Business Function element."""
        return BusinessElement(
            id=id,
            name=name,
            element_type="Function",
            layer=ArchiMateLayer.BUSINESS,
            aspect=ArchiMateAspect.BEHAVIOR,
            description=description,
            **kwargs
        )

    @staticmethod
    def create_business_interaction(
        id: str,
        name: str,
        description: Optional[str] = None,
        **kwargs
    ) -> BusinessElement:
        """Create a Business Interaction element."""
        return BusinessElement(
            id=id,
            name=name,
            element_type="Interaction",
            layer=ArchiMateLayer.BUSINESS,
            aspect=ArchiMateAspect.BEHAVIOR,
            description=description,
            **kwargs
        )

    @staticmethod
    def create_business_event(
        id: str,
        name: str,
        description: Optional[str] = None,
        **kwargs
    ) -> BusinessElement:
        """Create a Business Event element."""
        return BusinessElement(
            id=id,
            name=name,
            element_type="Event",
            layer=ArchiMateLayer.BUSINESS,
            aspect=ArchiMateAspect.BEHAVIOR,
            description=description,
            **kwargs
        )

    @staticmethod
    def create_business_service(
        id: str,
        name: str,
        description: Optional[str] = None,
        **kwargs
    ) -> BusinessElement:
        """Create a Business Service element."""
        return BusinessElement(
            id=id,
            name=name,
            element_type="Service",
            layer=ArchiMateLayer.BUSINESS,
            aspect=ArchiMateAspect.BEHAVIOR,
            description=description,
            **kwargs
        )

    @staticmethod
    def create_business_object(
        id: str,
        name: str,
        description: Optional[str] = None,
        **kwargs
    ) -> BusinessElement:
        """Create a Business Object element."""
        return BusinessElement(
            id=id,
            name=name,
            element_type="Object",
            layer=ArchiMateLayer.BUSINESS,
            aspect=ArchiMateAspect.PASSIVE_STRUCTURE,
            description=description,
            **kwargs
        )

    @staticmethod
    def create_business_contract(
        id: str,
        name: str,
        description: Optional[str] = None,
        **kwargs
    ) -> BusinessElement:
        """Create a Business Contract element."""
        return BusinessElement(
            id=id,
            name=name,
            element_type="Contract",
            layer=ArchiMateLayer.BUSINESS,
            aspect=ArchiMateAspect.PASSIVE_STRUCTURE,
            description=description,
            **kwargs
        )

    @staticmethod
    def create_business_representation(
        id: str,
        name: str,
        description: Optional[str] = None,
        **kwargs
    ) -> BusinessElement:
        """Create a Business Representation element."""
        return BusinessElement(
            id=id,
            name=name,
            element_type="Representation",
            layer=ArchiMateLayer.BUSINESS,
            aspect=ArchiMateAspect.PASSIVE_STRUCTURE,
            description=description,
            **kwargs
        )
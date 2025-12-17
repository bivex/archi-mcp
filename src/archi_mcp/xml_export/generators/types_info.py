"""ArchiMate types information utilities."""

from typing import Dict, List


class ArchiMateTypesInfo:
    """Provides information about supported ArchiMate types."""

    @staticmethod
    def get_supported_element_types() -> Dict[str, list]:
        """
        Get supported ArchiMate element types by layer.

        Returns:
            Dictionary mapping layers to element types
        """
        return {
            "Business": [
                "BusinessActor", "BusinessRole", "BusinessCollaboration",
                "BusinessInterface", "BusinessFunction", "BusinessProcess",
                "BusinessEvent", "BusinessService", "BusinessObject",
                "Contract", "Representation", "Location"
            ],
            "Application": [
                "ApplicationComponent", "ApplicationCollaboration",
                "ApplicationInterface", "ApplicationFunction",
                "ApplicationInteraction", "ApplicationProcess",
                "ApplicationEvent", "ApplicationService", "DataObject"
            ],
            "Technology": [
                "Node", "Device", "SystemSoftware", "TechnologyCollaboration",
                "TechnologyInterface", "Path", "CommunicationNetwork",
                "TechnologyFunction", "TechnologyProcess", "TechnologyInteraction",
                "TechnologyEvent", "TechnologyService", "Artifact"
            ],
            "Physical": [
                "Equipment", "Facility", "DistributionNetwork", "Material"
            ],
            "Motivation": [
                "Stakeholder", "Driver", "Assessment", "Goal", "Outcome",
                "Principle", "Requirement", "Constraint", "Meaning", "Value"
            ],
            "Strategy": [
                "Resource", "Capability", "CourseOfAction", "ValueStream"
            ],
            "Implementation": [
                "WorkPackage", "Deliverable", "ImplementationEvent",
                "Plateau", "Gap"
            ]
        }

    @staticmethod
    def get_supported_relationship_types() -> list:
        """
        Get supported ArchiMate relationship types.

        Returns:
            List of relationship type names
        """
        return [
            "AccessRelationship", "AggregationRelationship", "AssignmentRelationship",
            "AssociationRelationship", "CompositionRelationship", "FlowRelationship",
            "InfluenceRelationship", "RealizationRelationship", "ServingRelationship",
            "SpecializationRelationship", "TriggeringRelationship"
        ]

    @staticmethod
    def get_layer_for_element_type(element_type: str) -> str:
        """Get the layer for a given element type.

        Args:
            element_type: ArchiMate element type

        Returns:
            Layer name or empty string if not found
        """
        types_by_layer = ArchiMateTypesInfo.get_supported_element_types()
        for layer, types in types_by_layer.items():
            if element_type in types:
                return layer
        return ""

    @staticmethod
    def is_valid_element_type(element_type: str) -> bool:
        """Check if an element type is supported.

        Args:
            element_type: Element type to check

        Returns:
            True if the element type is supported
        """
        types_by_layer = ArchiMateTypesInfo.get_supported_element_types()
        for types in types_by_layer.values():
            if element_type in types:
                return True
        return False
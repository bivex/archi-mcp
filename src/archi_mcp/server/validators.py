# Copyright (c) 2025 Bivex
#
# Author: Bivex
# Available for contact via email: support@b-b.top
# For up-to-date contact information:
# https://github.com/bivex
#
# Created: 2025-12-18 11:23
# Last Updated: 2025-12-18 11:23
#
# Licensed under the MIT License.
# Commercial licensing available upon request.

"""Input validation and normalization functions for ArchiMate elements and relationships."""

from typing import Tuple, Dict, List
from ..types import ArchiMateRelationshipType
from ..archimate import ARCHIMATE_ELEMENTS, ARCHIMATE_RELATIONSHIPS
from .models import ElementInput, RelationshipInput


# Element type mapping for normalization
ELEMENT_TYPE_MAPPING: Dict[str, str] = {
    # Business Layer - normalize to internal format (with underscores)
    "BusinessActor": "Business_Actor",
    "Business_Actor": "Business_Actor",  # Identity mapping for correct format
    "BusinessRole": "Business_Role",
    "Business_Role": "Business_Role",  # Identity mapping
    "BusinessCollaboration": "Business_Collaboration",
    "Business_Collaboration": "Business_Collaboration",  # Identity mapping
    "BusinessInterface": "Business_Interface",
    "Business_Interface": "Business_Interface",  # Identity mapping
    "BusinessFunction": "Business_Function",
    "Business_Function": "Business_Function",  # Identity mapping
    "BusinessProcess": "Business_Process",
    "Business_Process": "Business_Process",  # Identity mapping
    "BusinessEvent": "Business_Event",
    "Business_Event": "Business_Event",  # Identity mapping
    "BusinessService": "Business_Service",
    "Business_Service": "Business_Service",  # Identity mapping
    "BusinessObject": "Business_Object",
    "Business_Object": "Business_Object",  # Identity mapping
    "Contract": "Contract",
    "Business_Contract": "Contract",  # Normalize to shorter form
    "Representation": "Representation",
    "Business_Representation": "Representation",  # Normalize to shorter form
    "Location": "Location",

    # Application Layer
    "ApplicationComponent": "Application_Component",
    "Application_Component": "Application_Component",  # Identity mapping
    "ApplicationCollaboration": "Application_Collaboration",
    "Application_Collaboration": "Application_Collaboration",  # Identity mapping
    "ApplicationInterface": "Application_Interface",
    "Application_Interface": "Application_Interface",  # Identity mapping
    "ApplicationFunction": "Application_Function",
    "Application_Function": "Application_Function",  # Identity mapping
    "ApplicationInteraction": "Application_Interaction",
    "Application_Interaction": "Application_Interaction",  # Identity mapping
    "ApplicationProcess": "Application_Process",
    "Application_Process": "Application_Process",  # Identity mapping
    "ApplicationEvent": "Application_Event",
    "Application_Event": "Application_Event",  # Identity mapping
    "ApplicationService": "Application_Service",
    "Application_Service": "Application_Service",  # Identity mapping
    "DataObject": "Data_Object",
    "Data_Object": "Data_Object",  # Identity mapping

    # Technology Layer
    "Node": "Node",
    "Device": "Device",
    "SystemSoftware": "System_Software",
    "System_Software": "System_Software",  # Identity mapping
    "TechnologyComponent": "Technology_Component",
    "Technology_Component": "Technology_Component",  # Identity mapping
    "TechnologyCollaboration": "Technology_Collaboration",
    "Technology_Collaboration": "Technology_Collaboration",  # Identity mapping
    "TechnologyInterface": "Technology_Interface",
    "Technology_Interface": "Technology_Interface",  # Identity mapping
    "TechnologyFunction": "Technology_Function",
    "Technology_Function": "Technology_Function",  # Identity mapping
    "TechnologyProcess": "Technology_Process",
    "Technology_Process": "Technology_Process",  # Identity mapping
    "TechnologyInteraction": "Technology_Interaction",
    "Technology_Interaction": "Technology_Interaction",  # Identity mapping
    "TechnologyEvent": "Technology_Event",
    "Technology_Event": "Technology_Event",  # Identity mapping
    "TechnologyService": "Technology_Service",
    "Technology_Service": "Technology_Service",  # Identity mapping
    "Artifact": "Artifact",
    "CommunicationNetwork": "Communication_Network",
    "Communication_Network": "Communication_Network",  # Identity mapping
    "Path": "Path",

    # Physical Layer
    "Equipment": "Equipment",
    "Facility": "Facility",
    "DistributionNetwork": "Distribution_Network",
    "Distribution_Network": "Distribution_Network",  # Identity mapping
    "Material": "Material",

    # Motivation Layer
    "Stakeholder": "Stakeholder",
    "Driver": "Driver",
    "Assessment": "Assessment",
    "Goal": "Goal",
    "Outcome": "Outcome",
    "Principle": "Principle",
    "Requirement": "Requirement",
    "Constraint": "Constraint",
    "Meaning": "Meaning",
    "Value": "Value",

    # Strategy Layer
    "Resource": "Resource",
    "Capability": "Capability",
    "CourseOfAction": "Course_of_Action",
    "Course_of_Action": "Course_of_Action",  # Identity mapping
    "ValueStream": "Value_Stream",
    "Value_Stream": "Value_Stream",  # Identity mapping

    # Implementation Layer
    "WorkPackage": "Work_Package",
    "Work_Package": "Work_Package",  # Identity mapping
    "Deliverable": "Deliverable",
    "ImplementationEvent": "Implementation_Event",
    "Implementation_Event": "Implementation_Event",  # Identity mapping
    "Plateau": "Plateau",
    "Gap": "Gap"
}


# Valid layers mapping
VALID_LAYERS: Dict[str, str] = {
    "business": "Business",
    "application": "Application",
    "technology": "Technology",
    "physical": "Physical",
    "motivation": "Motivation",
    "strategy": "Strategy",
    "implementation": "Implementation",
    # Allow both cases
    "Business": "Business",
    "Application": "Application",
    "Technology": "Technology",
    "Physical": "Physical",
    "Motivation": "Motivation",
    "Strategy": "Strategy",
    "Implementation": "Implementation"
}


# Valid relationship types
VALID_RELATIONSHIPS: List[str] = [
    "Access", "Aggregation", "Assignment", "Association", "Composition",
    "Flow", "Influence", "Realization", "Serving", "Specialization", "Triggering"
]


def normalize_element_type(element_type: str) -> str:
    """Normalize element type to canonical ArchiMate format."""
    # Handle common variations and prefixes
    element_type = element_type.strip()

    # Remove common prefixes if they exist
    for prefix in ["Business_", "Application_", "Technology_", "Physical_", "Motivation_", "Strategy_", "Implementation_"]:
        if element_type.startswith(prefix):
            element_type = element_type[len(prefix):]
            break

    # Apply canonical formatting
    element_type = element_type.replace(" ", "_").replace("-", "_")

    # Handle special cases
    type_mapping = {
        "Component": "Application_Component",
        "Service": "Business_Service",  # Default to Business Service
        "Interface": "Business_Interface",  # Default to Business Interface
        "Process": "Business_Process",  # Default to Business Process
        "Function": "Business_Function",  # Default to Business Function
        "Actor": "Business_Actor",
        "Role": "Business_Role",
        "Collaboration": "Business_Collaboration",
        "Event": "Business_Event",
        "Object": "Business_Object",
        "Contract": "Business_Contract",
        "Representation": "Business_Representation",
        "Interaction": "Business_Interaction",
        "Data_Object": "Application_DataObject",
        "System_Software": "Technology_SystemSoftware",
        "Artifact": "Technology_Artifact",
        "Device": "Technology_Device",
        "Node": "Technology_Node",
        "Path": "Technology_Path",
        "Communication_Network": "Technology_CommunicationNetwork",
        "Stakeholder": "Motivation_Stakeholder",
        "Driver": "Motivation_Driver",
        "Assessment": "Motivation_Assessment",
        "Goal": "Motivation_Goal",
        "Outcome": "Motivation_Outcome",
        "Principle": "Motivation_Principle",
        "Requirement": "Motivation_Requirement",
        "Constraint": "Motivation_Constraint",
        "Meaning": "Motivation_Meaning",
        "Value": "Motivation_Value",
        "Resource": "Strategy_Resource",
        "Capability": "Strategy_Capability",
        "Course_of_Action": "Strategy_CourseOfAction",
        "Value_Stream": "Strategy_ValueStream",
        "Work_Package": "Implementation_WorkPackage",
        "Deliverable": "Implementation_Deliverable",
        "Plateau": "Implementation_Plateau",
        "Gap": "Implementation_Gap",
        "Equipment": "Physical_Equipment",
        "Facility": "Physical_Facility",
        "Distribution_Network": "Physical_DistributionNetwork",
        "Material": "Physical_Material",
        "Location": "Business_Location"
    }

    return type_mapping.get(element_type, element_type)


def normalize_layer(layer: str) -> str:
    """Normalize layer name to canonical ArchiMate format."""
    layer = layer.strip().title()

    # Handle common variations
    layer_mapping = {
        "Business": "Business",
        "Application": "Application",
        "Technology": "Technology",
        "Physical": "Physical",
        "Motivation": "Motivation",
        "Strategy": "Strategy",
        "Implementation": "Implementation",
        # Handle lowercase variations
        "business": "Business",
        "application": "Application",
        "technology": "Technology",
        "physical": "Physical",
        "motivation": "Motivation",
        "strategy": "Strategy",
        "implementation": "Implementation"
    }

    return layer_mapping.get(layer, layer)


def normalize_relationship_type(rel_type: str) -> str:
    """Normalize relationship type to canonical ArchiMate format."""
    rel_type = rel_type.strip()

    # Handle common variations
    type_mapping = {
        "serving": "Serving",
        "Serving": "Serving",
        "realization": "Realization",
        "Realization": "Realization",
        "assignment": "Assignment",
        "Assignment": "Assignment",
        "access": "Access",
        "Access": "Access",
        "influence": "Influence",
        "Influence": "Influence",
        "triggering": "Triggering",
        "Triggering": "Triggering",
        "flow": "Flow",
        "Flow": "Flow",
        "specialization": "Specialization",
        "Specialization": "Specialization",
        "aggregation": "Aggregation",
        "Aggregation": "Aggregation",
        "composition": "Composition",
        "Composition": "Composition",
        "association": "Association",
        "Association": "Association"
    }

    return type_mapping.get(rel_type, rel_type)


def validate_element_input(element: ElementInput) -> Tuple[bool, str]:
    """Validate element input data."""
    try:
        # Check if element type exists in ArchiMate specification
        normalized_type = normalize_element_type(element.element_type)
        if normalized_type not in ARCHIMATE_ELEMENTS:
            return False, f"Unknown element type '{element.element_type}'. Valid types include: {', '.join(sorted(ARCHIMATE_ELEMENTS.keys())[:10])}..."

        # Check required fields
        if not element.id or not element.id.strip():
            return False, "Element ID is required and cannot be empty"

        if not element.name or not element.name.strip():
            return False, "Element name is required and cannot be empty"

        # Validate layer
        if element.layer not in ["Business", "Application", "Technology", "Physical", "Motivation", "Strategy", "Implementation"]:
            return False, f"Invalid layer '{element.layer}'. Valid layers: Business, Application, Technology, Physical, Motivation, Strategy, Implementation"

        return True, "Valid"

    except Exception as e:
        return False, f"Validation error: {str(e)}"


def validate_relationship_input(rel: RelationshipInput, language: str = "en") -> Tuple[bool, str]:
    """Validate relationship input data."""
    try:
        # Check if relationship type exists
        normalized_type = normalize_relationship_type(rel.relationship_type)
        if normalized_type not in ARCHIMATE_RELATIONSHIPS:
            return False, f"Unknown relationship type '{rel.relationship_type}'. Valid types: {', '.join(sorted(ARCHIMATE_RELATIONSHIPS.keys()))}"

        # Check required fields
        if not rel.id or not rel.id.strip():
            return False, "Relationship ID is required and cannot be empty"

        if not rel.from_element or not rel.from_element.strip():
            return False, "Source element ID is required and cannot be empty"

        if not rel.to_element or not rel.to_element.strip():
            return False, "Target element ID is required and cannot be empty"

        # Check for self-references
        if rel.from_element == rel.to_element:
            return False, "Relationship cannot reference the same element as both source and target"

        return True, "Valid"

    except Exception as e:
        return False, f"Validation error: {str(e)}"


def validate_relationship_name(custom_name: str, formal_relationship_type: str, language: str = "en") -> Tuple[bool, str]:
    """Validate custom relationship name against formal relationship type."""
    try:
        if not custom_name or not custom_name.strip():
            return False, "Relationship name cannot be empty"

        custom_name = custom_name.lower().strip()

        # Get synonyms for the formal relationship type
        formal_type = normalize_relationship_type(formal_relationship_type)

        # Define relationship type synonyms (this could be expanded)
        synonyms = {
            "serving": ["serves", "service", "provides service to", "provides service"],
            "realization": ["realizes", "implements", "is realized by", "realizes"],
            "assignment": ["assigned to", "is assigned to", "assignment"],
            "access": ["accesses", "can access", "has access to"],
            "influence": ["influences", "affects", "impacts"],
            "triggering": ["triggers", "starts", "initiates"],
            "flow": ["flows to", "flows", "data flow"],
            "specialization": ["specializes", "is a", "inherits from"],
            "aggregation": ["aggregates", "contains", "part of"],
            "composition": ["composes", "consists of", "composed of"],
            "association": ["associated with", "related to", "connects to"]
        }

        # Check if custom name matches any synonym
        valid_synonyms = synonyms.get(formal_type.lower(), [])
        if custom_name in [s.lower() for s in valid_synonyms]:
            return True, "Valid synonym"

        # Check for exact match with formal type
        if custom_name == formal_type.lower():
            return True, "Exact match"

        # Allow some flexibility for common variations
        if len(custom_name) > 50:
            return False, "Relationship name is too long (max 50 characters)"

        if len(custom_name.split()) > 5:
            return False, "Relationship name has too many words (max 5 words)"

        # For now, accept any reasonable name that doesn't match the restrictions above
        return True, "Accepted custom name"

    except Exception as e:
        return False, f"Validation error: {str(e)}"
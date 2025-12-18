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

"""ArchiMate XML Exchange Format Validator

Validates ArchiMate XML files against the Open Group schema.
Provides validation functionality for XML export testing.
"""

import logging
from typing import Optional, List, Dict, Any
from pathlib import Path

try:
    from lxml import etree
    LXML_AVAILABLE = True
except ImportError:
    import xml.etree.ElementTree as etree
    LXML_AVAILABLE = False

logger = logging.getLogger(__name__)


class ValidationError(Exception):
    """XML validation error."""
    pass


class ArchiMateXMLValidator:
    """
    ArchiMate XML Exchange Format Validator
    
    Validates XML files against ArchiMate 3.0 schema.
    This is a modular component for quality assurance.
    """
    
    def __init__(self):
        """Initialize the validator."""
        self.schema = None
        
    def validate_xml_string(self, xml_string: str) -> List[str]:
        """
        Validate XML string for basic well-formedness and structure.
        
        Args:
            xml_string: XML content to validate
            
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        try:
            # Parse XML
            if LXML_AVAILABLE:
                doc = etree.fromstring(xml_string.encode('utf-8'))
            else:
                doc = etree.fromstring(xml_string)
            
            # Basic structure validation
            errors.extend(self._validate_basic_structure(doc))
            
        except etree.XMLSyntaxError as e:
            errors.append(f"XML Syntax Error: {e}")
        except Exception as e:
            errors.append(f"Validation Error: {e}")
            
        return errors
    
    def validate_xml_file(self, file_path: Path) -> List[str]:
        """
        Validate XML file.
        
        Args:
            file_path: Path to XML file
            
        Returns:
            List of validation errors (empty if valid)
        """
        try:
            xml_content = file_path.read_text(encoding='utf-8')
            return self.validate_xml_string(xml_content)
        except Exception as e:
            return [f"File read error: {e}"]
    
    def _validate_basic_structure(self, root: etree.Element) -> List[str]:
        """Validate basic ArchiMate XML structure."""
        errors = []

        errors.extend(_validate_root_element(root))
        errors.extend(_validate_root_attributes(root))
        errors.extend(_validate_required_children(root))

        # Validate child sections
        errors.extend(_validate_child_sections(root, self))

        return errors

    def _validate_elements_section(self, elements_elem: etree.Element) -> List[str]:
        """Validate elements section."""
        errors = []
        element_ids = set()

        for element in elements_elem:
            element_errors = _validate_individual_element(element, element_ids, self)
            errors.extend(element_errors)

        return errors

    def _validate_relationships_section(self, relationships_elem: etree.Element) -> List[str]:
        """Validate relationships section."""
        errors = []
        relationship_ids = set()

        for relationship in relationships_elem:
            relationship_errors = _validate_individual_relationship(relationship, relationship_ids)
            errors.extend(relationship_errors)

        return errors

    def _find_child(self, parent: etree.Element, child_name: str) -> Optional[etree.Element]:
        """Find child element by name (namespace-aware)."""
        for child in parent:
            tag = child.tag.split('}')[-1] if '}' in child.tag else child.tag
            if tag == child_name:
                return child
        return None

    def get_validation_summary(self, errors: List[str]) -> Dict[str, Any]:
        """
        Get validation summary.

        Args:
            errors: List of validation errors

        Returns:
            Validation summary dictionary
        """
        return {
            'is_valid': len(errors) == 0,
            'error_count': len(errors),
            'errors': errors,
            'validator': 'ArchiMateXMLValidator'
        }


def _validate_root_element(root: etree.Element) -> List[str]:
    """Validate the root element tag."""
    errors = []
    if root.tag != "{http://www.opengroup.org/xsd/archimate/3.0/}model":
        if not root.tag.endswith("}model") and root.tag != "model":
            errors.append("Root element must be 'model'")
    return errors


def _validate_root_attributes(root: etree.Element) -> List[str]:
    """Validate required root element attributes."""
    errors = []
    if 'identifier' not in root.attrib:
        errors.append("Model element must have 'identifier' attribute")
    return errors


def _validate_required_children(root: etree.Element) -> List[str]:
    """Validate required child elements are present."""
    errors = []
    required_children = {'name', 'elements', 'relationships'}
    actual_children = set()

    for child in root:
        tag = child.tag
        # Remove namespace prefix if present
        if '}' in tag:
            tag = tag.split('}')[-1]
        actual_children.add(tag)

    missing_children = required_children - actual_children
    if missing_children:
        errors.append(f"Missing required child elements: {', '.join(missing_children)}")

    return errors


def _validate_child_sections(root: etree.Element, validator) -> List[str]:
    """Validate child sections (elements and relationships)."""
    errors = []

    # Validate elements section
    elements_elem = validator._find_child(root, 'elements')
    if elements_elem is not None:
        errors.extend(validator._validate_elements_section(elements_elem))

    # Validate relationships section
    relationships_elem = validator._find_child(root, 'relationships')
    if relationships_elem is not None:
        errors.extend(validator._validate_relationships_section(relationships_elem))

    return errors
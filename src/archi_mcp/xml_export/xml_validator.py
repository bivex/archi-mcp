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

"""
XML Schema and ArchiMate Relationship Validator

Provides validation for ArchiMate XML exports with:
1. XML schema validation (when XSD is available)
2. ArchiMate relationship matrix validation
3. Safe validation that never blocks export process
"""

import os
import subprocess
import tempfile
import logging
from typing import Dict, List, Tuple, Optional
from pathlib import Path
import re

from .archimate_relationship_matrix import validate_relationship, get_validation_suggestion

logger = logging.getLogger(__name__)

class ValidationResult:
    """Container for validation results."""
    
    def __init__(self):
        self.is_valid = True
        self.warnings: List[str] = []
        self.errors: List[str] = []
        self.suggestions: List[str] = []
        
    def add_warning(self, message: str):
        """Add validation warning."""
        self.warnings.append(message)
        
    def add_error(self, message: str):
        """Add validation error."""
        self.errors.append(message)
        self.is_valid = False
        
    def add_suggestion(self, message: str):
        """Add improvement suggestion."""
        self.suggestions.append(message)
        
    def get_summary(self) -> str:
        """Get validation summary."""
        lines = []

        lines.append(_get_validation_status(self.is_valid))
        lines.extend(_get_error_summary(self.errors))
        lines.extend(_get_warning_summary(self.warnings))
        lines.extend(_get_suggestion_summary(self.suggestions))

        return "\n".join(lines)


def _get_validation_status(is_valid: bool) -> str:
    """Get validation status line."""
    if is_valid:
        return "✅ VALIDATION PASSED"
    else:
        return "❌ VALIDATION FAILED"


def _get_error_summary(errors: List[str]) -> List[str]:
    """Get error summary section."""
    lines = []
    if errors:
        lines.append(f"\n🚨 Errors ({len(errors)}):")
        for error in errors:
            lines.append(f"  - {error}")
    return lines


def _get_warning_summary(warnings: List[str]) -> List[str]:
    """Get warning summary section."""
    lines = []
    if warnings:
        lines.append(f"\n⚠️  Warnings ({len(warnings)}):")
        for warning in warnings:
            lines.append(f"  - {warning}")
    return lines


def _get_suggestion_summary(suggestions: List[str]) -> List[str]:
    """Get suggestion summary section."""
    lines = []
    if suggestions:
        lines.append(f"\n💡 Suggestions ({len(suggestions)}):")
        for suggestion in suggestions:
            lines.append(f"  - {suggestion}")
    return lines

class ArchiMateXMLValidator:
    """
    ArchiMate XML validator with safe validation approach.
    
    Never blocks export process - only provides warnings and suggestions.
    """
    
    def __init__(self, enable_xmllint: bool = None):
        """
        Initialize validator.
        
        Args:
            enable_xmllint: Enable xmllint validation (auto-detect if None)
        """
        self.enable_xmllint = enable_xmllint
        if enable_xmllint is None:
            self.enable_xmllint = self._check_xmllint_available()
            
    def _check_xmllint_available(self) -> bool:
        """Check if xmllint is available on system."""
        try:
            result = subprocess.run(
                ["xmllint", "--version"], 
                capture_output=True, 
                text=True, 
                timeout=5
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
            
    def validate_xml_file(self, xml_file_path: str) -> ValidationResult:
        """
        Validate ArchiMate XML file.
        
        Args:
            xml_file_path: Path to XML file to validate
            
        Returns:
            ValidationResult with validation findings
        """
        result = ValidationResult()
        
        try:
            # Read XML content
            with open(xml_file_path, 'r', encoding='utf-8') as f:
                xml_content = f.read()
                
            # Validate XML structure
            self._validate_xml_structure(xml_content, result)
            
            # Validate ArchiMate relationships
            self._validate_archimate_relationships(xml_content, result)
            
            # Optional xmllint validation
            if self.enable_xmllint:
                self._validate_with_xmllint(xml_file_path, result)
                
        except Exception as e:
            logger.error(f"Validation error: {e}")
            result.add_warning(f"Validation failed with error: {str(e)}")
            
        return result
        
    def validate_xml_content(self, xml_content: str) -> ValidationResult:
        """
        Validate ArchiMate XML content string.
        
        Args:
            xml_content: XML content to validate
            
        Returns:
            ValidationResult with validation findings
        """
        result = ValidationResult()
        
        try:
            # Validate XML structure
            self._validate_xml_structure(xml_content, result)
            
            # Validate ArchiMate relationships
            self._validate_archimate_relationships(xml_content, result)
            
            # Optional xmllint validation via temp file
            if self.enable_xmllint:
                with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False, encoding='utf-8') as f:
                    f.write(xml_content)
                    temp_path = f.name
                    
                try:
                    self._validate_with_xmllint(temp_path, result)
                finally:
                    os.unlink(temp_path)
                    
        except Exception as e:
            logger.error(f"Validation error: {e}")
            result.add_warning(f"Validation failed with error: {str(e)}")
            
        return result
        
    def _validate_xml_structure(self, xml_content: str, result: ValidationResult):
        """Validate basic XML structure."""
        
        # Check XML declaration
        if not xml_content.strip().startswith('<?xml'):
            result.add_warning("Missing XML declaration")
            
        # Check for required ArchiMate namespace
        if 'xmlns:archimate=' not in xml_content:
            result.add_error("Missing ArchiMate namespace declaration")
            
        # Check root element
        if '<archimate:model' not in xml_content:
            result.add_error("Missing ArchiMate model root element")
            
        # Check for Views folder (required for Archi import)
        if 'type="diagrams"' not in xml_content:
            result.add_warning("Missing Views folder - diagram may not display in Archi")
            
    def _validate_archimate_relationships(self, xml_content: str, result: ValidationResult):
        """Validate ArchiMate relationships using relationship matrix."""
        
        # Extract relationships
        rel_pattern = r'<element xsi:type="archimate:(\w+Relationship)" id="([^"]+)" source="([^"]+)" target="([^"]+)"'
        relationships = re.findall(rel_pattern, xml_content)
        
        # Extract elements
        elem_pattern = r'<element xsi:type="archimate:(\w+)" id="([^"]+)" name="([^"]*)"'
        elements = re.findall(elem_pattern, xml_content)
        
        # Build element type lookup
        element_types = {elem_id: elem_type for elem_type, elem_id, name in elements}
        
        # Validate each relationship
        invalid_count = 0
        for rel_type, rel_id, source_id, target_id in relationships:
            source_type = element_types.get(source_id, "Unknown")
            target_type = element_types.get(target_id, "Unknown")
            
            if source_type == "Unknown" or target_type == "Unknown":
                result.add_warning(f"Relationship {rel_id}: Unknown element type")
                continue
                
            # Validate relationship
            is_valid = validate_relationship(source_type, target_type, rel_type)
            
            if not is_valid:
                invalid_count += 1
                suggestion = get_validation_suggestion(source_type, target_type, rel_type)
                result.add_error(f"Invalid relationship {rel_id}: {source_type} --[{rel_type}]--> {target_type}")
                result.add_suggestion(f"For {rel_id}: {suggestion}")
                
        if invalid_count > 0:
            result.add_error(f"Found {invalid_count} invalid relationships according to ArchiMate 3.2 specification")
        else:
            result.add_suggestion("All relationships are valid according to ArchiMate 3.2 specification")
            
    def _validate_with_xmllint(self, xml_file_path: str, result: ValidationResult):
        """Validate XML using xmllint (if available)."""
        
        try:
            # Basic well-formedness check
            cmd = ["xmllint", "--noout", xml_file_path]
            process_result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if process_result.returncode == 0:
                result.add_suggestion("XML is well-formed (xmllint check passed)")
            else:
                # Parse xmllint errors
                errors = process_result.stderr.strip()
                if errors:
                    result.add_warning(f"xmllint validation issues: {errors}")
                else:
                    result.add_warning("xmllint validation failed (unknown reason)")
                    
        except subprocess.TimeoutExpired:
            result.add_warning("xmllint validation timed out")
        except Exception as e:
            result.add_warning(f"xmllint validation error: {str(e)}")

    def validate_xml_string(self, xml_content: str) -> List[str]:
        """
        Validate XML string and return list of errors.

        Args:
            xml_content: XML content to validate

        Returns:
            List of validation error messages
        """
        result = self.validate_xml_content(xml_content)
        return result.errors + result.warnings

    def get_validation_summary(self, errors: List[str]) -> Dict:
        """
        Generate validation summary from error list.

        Args:
            errors: List of validation errors

        Returns:
            Dictionary with validation summary
        """
        return {
            'is_valid': len(errors) == 0,
            'error_count': len(errors),
            'errors': errors,
            'validator': 'ArchiMateXMLValidator'
        }


# Environment-controlled validation
def is_validation_enabled() -> bool:
    """Check if validation is enabled via environment variable."""
    # Enable by default for better user experience (can be disabled if needed)
    return os.getenv("ARCHI_MCP_ENABLE_VALIDATION", "true").lower() in ("true", "1", "yes")

def validate_archimate_export(xml_file_path: str) -> Optional[ValidationResult]:
    """
    Validate ArchiMate export if validation is enabled.
    
    Args:
        xml_file_path: Path to exported XML file
        
    Returns:
        ValidationResult if validation enabled, None otherwise
    """
    if not is_validation_enabled():
        return None
        
    validator = ArchiMateXMLValidator()
    return validator.validate_xml_file(xml_file_path)

def log_validation_results(result: ValidationResult, logger_instance: logging.Logger = None):
    """Log validation results."""
    logger_instance = logger_instance or logger

    _log_validation_status(result, logger_instance)
    _log_validation_errors(result, logger_instance)
    _log_validation_warnings(result, logger_instance)
    _log_validation_suggestions(result, logger_instance)


def _log_validation_status(result: ValidationResult, logger_instance: logging.Logger):
    """Log overall validation status."""
    if result.is_valid:
        logger_instance.info("XML validation passed")
    else:
        logger_instance.warning("XML validation found issues")


def _log_validation_errors(result: ValidationResult, logger_instance: logging.Logger):
    """Log validation errors."""
    if result.errors:
        for error in result.errors:
            logger_instance.error(f"Validation error: {error}")


def _log_validation_warnings(result: ValidationResult, logger_instance: logging.Logger):
    """Log validation warnings."""
    if result.warnings:
        for warning in result.warnings:
            logger_instance.warning(f"Validation warning: {warning}")


def _log_validation_suggestions(result: ValidationResult, logger_instance: logging.Logger):
    """Log validation suggestions."""
    if result.suggestions:
        for suggestion in result.suggestions:
            logger_instance.info(f"Validation suggestion: {suggestion}")
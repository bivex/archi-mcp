# Copyright (c) 2025 Bivex
#
# Author: Bivex
# Available for contact via email: support@b-b.top
# For up-to-date contact information:
# https://github.com/bivex
#
# Created: 2025-12-18T11:40:30
# Last Updated: 2025-12-18T11:40:30
#
# Licensed under the MIT License.
# Commercial licensing available upon request.

"""Structured response models for FastMCP tools with automatic schema generation."""

from dataclasses import dataclass
from typing import Dict, List, Optional
from pydantic import BaseModel, Field


@dataclass
class DiagramEnhancementRequest:
    """Request for additional diagram enhancement details."""
    add_legend: bool
    theme_preference: Optional[str] = None
    additional_notes: Optional[str] = None


@dataclass
class DiagramFiles:
    """Information about generated diagram files."""
    plantuml: str
    png: str
    svg: Optional[str] = None


@dataclass
class DiagramGenerationResponse:
    """Structured response for diagram generation operations."""
    success: bool
    message: str
    export_directory: str
    files: DiagramFiles
    debug_log: Optional[List[str]] = None


@dataclass
class FileLoadResponse:
    """Structured response for file loading operations."""
    success: bool
    message: str
    file_path: str
    diagram_title: Optional[str] = None
    element_count: Optional[int] = None
    relationship_count: Optional[int] = None
    group_count: Optional[int] = None


@dataclass
class GroupsTestResponse:
    """Structured response for groups functionality testing."""
    success: bool
    message: str
    groups_created: int
    elements_assigned: int
    relationships_created: int
    nested_groups: int
    files: DiagramFiles
    features_tested: List[str]


# Pydantic models for more complex responses if needed
class ErrorResponse(BaseModel):
    """Structured error response model."""
    success: bool = Field(default=False, description="Whether the operation succeeded")
    message: str = Field(..., description="Error message")
    error_type: Optional[str] = Field(None, description="Type of error that occurred")
    details: Optional[Dict[str, str]] = Field(None, description="Additional error details")
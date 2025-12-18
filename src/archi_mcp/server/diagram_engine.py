# Copyright (c) 2025 Bivex
#
# Author: Bivex
# Available for contact via email: support@b-b.top
# For up-to-date contact information:
# https://github.com/bivex
#
# Created: 2025-12-18 11:24
# Last Updated: 2025-12-18 11:24
#
# Licensed under the MIT License.
# Commercial licensing available upon request.

"""Core diagram processing engine for ArchiMate MCP server."""

# VERIFIED ✅ - PlantUML validation implemented

import os
import json
import base64
import zlib
import time
import platform
import subprocess
import tempfile
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from ..utils.logging import get_logger
from ..utils.exceptions import ArchiMateError
from ..utils.json_parser import parse_json_string
from ..i18n import ArchiMateTranslator
from ..archimate import ArchiMateGenerator, ArchiMateValidator
from ..archimate.generator import DiagramLayout
from .models import DiagramInput
from .config import get_layout_setting
from .language import detect_language_from_content, translate_relationship_labels
from .plantuml_validator import validate_plantuml_renders, validate_png_file, find_plantuml_jar, setup_java_environment
from .export_manager import get_exports_directory, create_export_directory, cleanup_failed_exports
from .error_handler import build_enhanced_error_response

logger = get_logger(__name__)


def _setup_language_and_translator(diagram: DiagramInput, debug_log: list) -> Tuple[str, ArchiMateTranslator, ArchiMateGenerator]:
    """Setup language detection and translation for diagram processing."""
    # Detect language from diagram content
    language = detect_language_from_content(diagram)
    debug_log.append(f"Detected language: {language}")

    # Create translator for the detected language
    translator = ArchiMateTranslator(language)

    # Create generator with translator
    generator = ArchiMateGenerator(translator=translator)

    return language, translator, generator


def _configure_layout(diagram: DiagramInput, debug_log: list) -> DiagramLayout:
    """Configure diagram layout based on environment settings and diagram input."""
    # Get layout configuration
    layout_config = diagram.layout or {}

    # Auto-enable group_by_groups if diagram contains groups
    has_groups = len(diagram.groups) > 0
    group_by_groups = layout_config.get("group_by_groups", has_groups)

    # Create layout object with defaults from environment
    layout = DiagramLayout(
        direction=get_layout_setting("ARCHI_MCP_DEFAULT_DIRECTION", layout_config.get("direction")),
        show_legend=get_layout_setting("ARCHI_MCP_DEFAULT_SHOW_LEGEND", layout_config.get("show_legend")),
        show_title=get_layout_setting("ARCHI_MCP_DEFAULT_SHOW_TITLE", layout_config.get("show_title")),
        group_by_layer=get_layout_setting("ARCHI_MCP_DEFAULT_GROUP_BY_LAYER", layout_config.get("group_by_layer")),
        spacing=get_layout_setting("ARCHI_MCP_DEFAULT_SPACING", layout_config.get("spacing")),
        show_element_types=get_layout_setting("ARCHI_MCP_DEFAULT_SHOW_ELEMENT_TYPES", layout_config.get("show_element_types")),
        show_relationship_labels=get_layout_setting("ARCHI_MCP_DEFAULT_SHOW_RELATIONSHIP_LABELS", layout_config.get("show_relationship_labels")),
        group_by_groups=group_by_groups
    )

    debug_log.append(f"Layout configuration: {layout.model_dump()}")

    return layout


def _process_elements(generator: ArchiMateGenerator, diagram: DiagramInput, language: str, debug_log: list):
    """Process and add elements to the generator."""
    debug_log.append(f"Processing {len(diagram.elements)} elements")

    from ..archimate.elements.base import ArchiMateElement, ArchiMateLayer, ArchiMateAspect

    for element_data in diagram.elements:
        try:
            # Create element from input data
            # Convert layer and aspect strings to enums
            layer = ArchiMateLayer(element_data.layer) if hasattr(ArchiMateLayer, element_data.layer) else ArchiMateLayer.BUSINESS
            aspect = ArchiMateAspect(element_data.aspect) if element_data.aspect and hasattr(ArchiMateAspect, element_data.aspect) else ArchiMateAspect.ACTIVE_STRUCTURE

            element = ArchiMateElement(
                id=element_data.id,
                name=element_data.name,
                element_type=element_data.element_type,
                layer=layer,
                aspect=aspect,
                description=element_data.description,
                group_id=element_data.group_id
            )
            generator.add_element(element)
            debug_log.append(f"Added element: {element.id} ({element.element_type})")
        except Exception as e:
            debug_log.append(f"Error adding element {element_data.id}: {e}")
            raise ArchiMateError(f"Failed to add element {element_data.id}: {e}")


def _process_relationships(generator: ArchiMateGenerator, diagram: DiagramInput, language: str, debug_log: list):
    """Process and add relationships to the generator."""
    debug_log.append(f"Processing {len(diagram.relationships)} relationships")

    from ..archimate.relationships import ArchiMateRelationship
    from ..archimate.relationships.types import ArchiMateRelationshipType

    for rel_data in diagram.relationships:
        try:
            # Create relationship from input data
            relationship = ArchiMateRelationship(
                id=rel_data.id,
                from_element=rel_data.from_element,
                to_element=rel_data.to_element,
                relationship_type=ArchiMateRelationshipType(rel_data.relationship_type),
                description=rel_data.description,
                label=rel_data.label,
                length=rel_data.length,
                line_style=rel_data.line_style,
                color=rel_data.color,
                orientation=rel_data.orientation,
                positioning=rel_data.positioning
            )
            generator.add_relationship(relationship)
            debug_log.append(f"Added relationship: {relationship.id} ({relationship.relationship_type})")
        except Exception as e:
            debug_log.append(f"Error adding relationship {rel_data.id}: {e}")
            raise ArchiMateError(f"Failed to add relationship {rel_data.id}: {e}")


def _process_groups(generator: ArchiMateGenerator, diagram: DiagramInput, debug_log: list):
    """Process and add groups to the generator."""
    debug_log.append(f"Processing {len(diagram.groups)} groups")

    from ..archimate.elements.base import ArchiMateGroup, ComponentGroupingStyle

    for group_data in diagram.groups:
        try:
            # Create group from input data
            group = ArchiMateGroup(
                id=group_data.id,
                name=group_data.name,
                group_type=ComponentGroupingStyle(group_data.group_type),
                parent_group_id=group_data.parent_group_id,
                description=group_data.description,
                properties=group_data.properties
            )
            generator.add_group(group)
            debug_log.append(f"Added group: {group.id} ({group.group_type.value})")
        except Exception as e:
            debug_log.append(f"Error adding group {group_data.id}: {e}")
            raise ArchiMateError(f"Failed to add group {group_data.id}: {e}")


def _generate_and_validate_plantuml(generator: ArchiMateGenerator, title: str, description: str, debug_log: list) -> str:
    """Generate PlantUML code and validate it can render."""
    # Generate PlantUML code
    debug_log.append("Generating PlantUML code")
    plantuml_code = generator.generate_plantuml(title=title, description=description)

    # Validate that the PlantUML code can render
    debug_log.append("Validating PlantUML code")
    valid, error_msg = validate_plantuml_renders(plantuml_code)

    if not valid:
        debug_log.append(f"PlantUML validation failed: {error_msg}")
        raise ArchiMateError(f"Generated PlantUML code is invalid: {error_msg}")

    debug_log.append("PlantUML code validation successful")
    return plantuml_code


def _generate_images(plantuml_code: str, plantuml_jar: str, debug_log: list) -> Tuple[str, str]:
    """Generate PNG and SVG images from PlantUML code."""
    debug_log.append("Generating images from PlantUML code")

    # Setup Java environment
    setup_java_environment()

    # Create temporary files for PlantUML processing
    with tempfile.NamedTemporaryFile(mode='w', suffix='.puml', delete=False) as temp_file:
        temp_file.write(plantuml_code)
        temp_file_path = temp_file.name

    try:
        # Generate PNG in background
        png_file_path = temp_file_path.replace('.puml', '.png')
        cmd_png = ['java', '-jar', plantuml_jar, '-tpng', temp_file_path]

        debug_log.append(f"Running PlantUML PNG generation: {' '.join(cmd_png)}")
        png_process = subprocess.Popen(
            cmd_png,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Generate SVG in background (parallel with PNG)
        svg_file_path = temp_file_path.replace('.puml', '.svg')
        cmd_svg = ['java', '-jar', plantuml_jar, '-tsvg', temp_file_path]

        debug_log.append(f"Running PlantUML SVG generation: {' '.join(cmd_svg)}")
        svg_process = subprocess.Popen(
            cmd_svg,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Wait for PNG process with timeout
        try:
            png_process.wait(timeout=60)
            if png_process.returncode != 0:
                _, stderr = png_process.communicate()
                error_msg = stderr.strip() if stderr else "Unknown error"
                debug_log.append(f"PNG generation failed: {error_msg}")
                if "Unable to locate a Java Runtime" in error_msg:
                    raise ArchiMateError("Failed to generate PNG: Java runtime not found. Please install Java (OpenJDK) to use PlantUML. On macOS: 'brew install openjdk'. On Ubuntu/Debian: 'sudo apt install openjdk-21-jdk'.")
                raise ArchiMateError(f"Failed to generate PNG: {error_msg}")
        except subprocess.TimeoutExpired:
            png_process.kill()
            debug_log.append("PNG generation timed out")
            raise ArchiMateError("PNG generation timed out (60 seconds)")

        # Validate PNG file
        png_valid, png_msg = validate_png_file(Path(png_file_path))
        if not png_valid:
            debug_log.append(f"PNG validation failed: {png_msg}")
            raise ArchiMateError(f"Generated PNG is invalid: {png_msg}")

        debug_log.append(f"PNG generation successful: {png_file_path}")

        # Wait for SVG process (no timeout needed since PNG succeeded)
        svg_process.wait()
        svg_generated = False
        if svg_process.returncode == 0 and os.path.exists(svg_file_path):
            svg_generated = True
            debug_log.append(f"SVG generation successful: {svg_file_path}")
        else:
            debug_log.append("SVG generation failed or not supported")

        return png_file_path, svg_file_path if svg_generated else None

    except subprocess.TimeoutExpired:
        debug_log.append("Image generation timed out")
        raise ArchiMateError("Image generation timed out (60 seconds)")
    finally:
        # Clean up temporary PlantUML file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)


def _export_diagram_files(plantuml_code: str, png_file_path: str, svg_file_path: str,
                         export_dir: Path, title: str, debug_log: list) -> Tuple[str, str, str, bool]:
    """Export diagram files to the export directory."""
    debug_log.append(f"Exporting files to: {export_dir}")

    # Generate safe filename from title
    safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
    safe_title = safe_title.replace(' ', '_')

    # Export PlantUML code
    puml_filename = f"{safe_title}.puml"
    puml_path = export_dir / puml_filename
    with open(puml_path, 'w', encoding='utf-8') as f:
        f.write(plantuml_code)
    debug_log.append(f"Exported PlantUML: {puml_path}")

    # Export PNG
    png_filename = f"{safe_title}.png"
    png_export_path = export_dir / png_filename
    os.rename(png_file_path, png_export_path)
    debug_log.append(f"Exported PNG: {png_export_path}")

    # Export SVG if available
    svg_export_path = None
    svg_generated = False
    if svg_file_path and os.path.exists(svg_file_path):
        svg_filename = f"{safe_title}.svg"
        svg_export_path = export_dir / svg_filename
        os.rename(svg_file_path, svg_export_path)
        svg_generated = True
        debug_log.append(f"Exported SVG: {svg_export_path}")
    elif svg_file_path:
        os.remove(svg_file_path)  # Clean up if file exists but we don't use it

    return str(puml_path), str(png_export_path), str(svg_export_path) if svg_generated else None, svg_generated


def _generate_success_response(export_dir: Path, svg_generated: bool,
                              puml_path: str, png_path: str, svg_path: str = None,
                              debug_log: list = None) -> str:
    """Generate success response with file information."""
    response = {
        "success": True,
        "message": "ArchiMate diagram generated successfully",
        "export_directory": str(export_dir),
        "files": {
            "plantuml": puml_path,
            "png": png_path
        }
    }

    if svg_generated and svg_path:
        response["files"]["svg"] = svg_path

    # Add debug information if available
    if debug_log:
        response["debug_log"] = debug_log

    return json.dumps(response, indent=2, ensure_ascii=False)


def save_debug_log(export_dir: Path, log_entries: List[Dict[str, Any]]) -> Path:
    """Save debug log to export directory."""
    debug_log_path = export_dir / "debug_log.json"
    with open(debug_log_path, 'w', encoding='utf-8') as f:
        json.dump(log_entries, f, indent=2, ensure_ascii=False, default=str)
    return debug_log_path


def _save_failed_attempt(plantuml_code: str, diagram_input: DiagramInput, debug_log: list, error_message: str) -> None:
    """Save failed attempt data for debugging."""
    try:
        export_dir = create_export_directory()
        debug_log_path = save_debug_log(export_dir, debug_log)

        # Save PlantUML code
        failed_puml_path = export_dir / "failed_diagram.puml"
        with open(failed_puml_path, 'w', encoding='utf-8') as f:
            f.write(plantuml_code)

        # Save input data
        failed_input_path = export_dir / "failed_input.json"
        with open(failed_input_path, 'w', encoding='utf-8') as f:
            json.dump(diagram_input.model_dump(), f, indent=2, ensure_ascii=False)

        logger.warning(f"Failed attempt saved to: {export_dir}")
        logger.warning(f"Error: {error_message}")

    except Exception as log_error:
        logger.warning(f"Could not save debug log: {log_error}")


def create_archimate_diagram_impl(diagram: DiagramInput) -> str:
    """Generate production-ready ArchiMate diagrams with comprehensive styling and layout options.

    This is the main MCP tool for creating ArchiMate diagrams. It provides extensive capabilities
    for defining and visualizing architectural models using the ArchiMate framework with PlantUML.

    Features include:
    - Comprehensive styling with 6 visual themes (Modern, Classic, Colorful, Minimal, Dark, Professional)
    - Hierarchical grouping of elements by layers and aspects
    - Rich component diagram features (ports, interfaces, notes)
    - Advanced relationship styling with custom arrow types and directions
    - Multi-language support for element and relationship labels (English, Russian, Slovak, Ukrainian)
    - Export capabilities to PNG, SVG, and raw PlantUML code

    AVAILABLE ELEMENTS BY LAYER:
    • Business Layer: Actor, Role, Collaboration, Interface, Process, Function, Interaction, Event, Service, Object, Contract, Representation
    • Application Layer: Component, Interface, Function, Interaction, Service, Data Object
    • Technology Layer: Node, Device, System Software, Technology Interface, Technology Function, Technology Service, Artifact
    • Physical Layer: Equipment, Facility, Distribution Network, Material
    • Motivation Layer: Stakeholder, Driver, Assessment, Goal, Outcome, Principle, Requirement, Constraint
    • Strategy Layer: Capability, Resource, Course of Action
    • Implementation Layer: Work Package, Deliverable, Implementation Event, Plateau

    VISUAL THEMES:
    • MODERN: Clean, contemporary design with blue accents.
    • CLASSIC: Traditional styling with gray tones.
    • COLORFUL: Bright, vibrant color scheme.
    • MINIMAL: Clean, minimal design with subtle styling.
    • DARK: Dark theme suitable for presentations.
    • PROFESSIONAL: Corporate styling with professional colors.

    ADVANCED FEATURES:
    • Ports & Interfaces: Define connection points and expose interfaces for components.
    • Notes: Attach descriptive notes to elements, customize position and colors.
    • Grouping Styles: Utilize various PlantUML grouping constructs: `package`, `node`, `folder`, `frame`, `cloud`, `database`, `rectangle`.
    • Relationship Styles: Control arrow appearance with `solid`, `dashed`, `dotted` lines and specific arrowheads (e.g., `COMPOSITION`, `AGGREGATION`, `SERVING`).
    • Layout Controls: Fine-tune diagram layout with direction hints (`horizontal`, `vertical`), spacing options (`compact`, `normal`, `wide`), and advanced Graphviz engine pragmas (`layout_engine`, `concentrate`, `nodesep`, `ranksep`).
    • Sprites in Stereotypes: Use custom PlantUML sprites with `$sprite_name` syntax (e.g., `<<$businessProcess>>`) for visual stereotypes.
    • JSON Data Display: Embed JSON data objects in diagrams with automatic `allowmixing` directive for mixed diagram types.
    • Advanced Hide/Remove System: Use `$tags` for selective element visibility control with `hide $tag` and `remove $tag` operations. Also supports `hide_unlinked` and `remove_unlinked` for automatic handling of elements without relationships, and `remove_all_tagged` for wildcard removal of all tagged elements with selective restore.
    • Long Descriptions: Multi-line component descriptions using bracket syntax `[long description here]` for detailed documentation.
    • Enhanced Arrow Control: Full directional control with length modifiers (1-5), line styles (solid/dashed/dotted), custom colors, orientation modes (vertical/horizontal/dot), and positioning hints (`hidden` relationships).
    • Component-Specific Styling: Advanced skinparam customization with component-style variants (`uml1`, `uml2`, `rectangle`).
    • Naming Rules: Components with names starting with '$' require an alias or tag to be hideable/removable (PlantUML limitation).
    • Note Definition: Notes must be defined within element objects using the 'notes' array, not as separate elements. Example: {"id": "comp1", "notes": [{"content": "Important note", "position": "right"}]}
    • Sprites in Stereotypes: Use custom PlantUML sprites with `$sprite_name` syntax (e.g., `<<$businessProcess>>`) for visual stereotypes.
    • JSON Data Display: Embed JSON data objects in diagrams with automatic `allowmixing` directive for mixed diagram types.
    • Advanced Hide/Remove System: Use `$tags` for selective element visibility control with `hide $tag` and `remove $tag` operations. Also supports `hide_unlinked` and `remove_unlinked` for automatic handling of elements without relationships, and `remove_all_tagged` for wildcard removal of all tagged elements with selective restore.
    • Long Descriptions: Multi-line component descriptions using bracket syntax `[long description here]` for detailed documentation.
    • Enhanced Arrow Control: Full directional control with length modifiers (1-5), line styles (solid/dashed/dotted), custom colors, orientation modes (vertical/horizontal/dot), and positioning hints (`hidden` relationships).
    • Component-Specific Styling: Advanced skinparam customization with component-style variants (`uml1`, `uml2`, `rectangle`).
    • Naming Rules: Components with names starting with '$' require an alias or tag to be hideable/removable (PlantUML limitation).
    • Note Definition: Notes must be defined within element objects using the 'notes' array, not as separate elements. Example: {"id": "comp1", "notes": [{"content": "Important note", "position": "right"}]}

    Args:
        diagram: A `DiagramInput` object containing the specification for the diagram.
                 This includes elements, relationships, layout, and output configurations.

    Returns:
        A JSON string containing the generated PlantUML code and paths to exported images (PNG, SVG).

    Raises:
        ArchiMateError: If diagram generation or validation fails.
    """
    debug_log = []
    start_time = time.time()

    try:
        logger.info("Starting ArchiMate diagram creation")
        debug_log.append(f"Started at: {datetime.now().isoformat()}")

        # Setup language and translator
        language, translator, generator = _setup_language_and_translator(diagram, debug_log)

        # Apply relationship label translations
        translate_relationship_labels(diagram, translator)

        # Configure layout
        layout = _configure_layout(diagram, debug_log)
        generator.set_layout(layout)

        # Configure hide/remove unlinked elements
        layout_config = diagram.layout or {}
        if layout_config.get("hide_unlinked", False):
            generator.hide_unlinked_elements()
            debug_log.append("Hide unlinked elements enabled")
        elif layout_config.get("remove_unlinked", False):
            generator.remove_unlinked_elements()
            debug_log.append("Remove unlinked elements enabled")

        # Configure remove all tagged elements (wildcard)
        if layout_config.get("remove_all_tagged", False):
            generator.remove_all_tagged_elements()
            debug_log.append("Remove all tagged elements (wildcard) enabled")

        # Process elements, groups and relationships
        _process_elements(generator, diagram, language, debug_log)
        _process_groups(generator, diagram, debug_log)
        _process_relationships(generator, diagram, language, debug_log)

        # Generate and validate PlantUML
        title = diagram.title or "ArchiMate Diagram"
        description = diagram.description or ""
        plantuml_code = _generate_and_validate_plantuml(generator, title, description, debug_log)

        # Find PlantUML JAR
        plantuml_jar = find_plantuml_jar(debug_log)
        if not plantuml_jar:
            raise ArchiMateError("PlantUML JAR not found. Please install PlantUML.")

        # Generate images
        png_file_path, svg_file_path = _generate_images(plantuml_code, plantuml_jar, debug_log)

        # Create export directory
        export_dir = create_export_directory()

        # Export files
        puml_path, png_path, svg_path, svg_generated = _export_diagram_files(
            plantuml_code, png_file_path, svg_file_path, export_dir, title, debug_log
        )

        # Generate success response
        processing_time = time.time() - start_time
        debug_log.append(f"Total processing time: {processing_time:.2f} seconds")

        response = _generate_success_response(export_dir, svg_generated, puml_path, png_path, svg_path, debug_log)

        logger.info(f"ArchiMate diagram created successfully in {processing_time:.2f} seconds")
        return response

    except Exception as e:
        logger.error(f"Error creating ArchiMate diagram: {e}")

        # Save failed attempt data
        _save_failed_attempt(plantuml_code if 'plantuml_code' in locals() else "", diagram, debug_log, str(e))

        # Build enhanced error response
        enhanced_error = build_enhanced_error_response(e, debug_log, None, locals().get('plantuml_code'))
        raise ArchiMateError(enhanced_error)


def load_diagram_from_file_impl(file_path: str) -> str:
    """Implementation of load diagram from file."""
    try:
        from pathlib import Path

        # Resolve file path
        json_file = Path(file_path)
        if not json_file.is_absolute():
            # Try relative to current directory
            json_file = Path.cwd() / file_path

        # Check if file exists
        if not json_file.exists():
            return f"❌ Error: File not found: {json_file}\n\nSearched in: {Path.cwd()}"

        # Read file
        logger.info(f"Loading diagram from file: {json_file}")
        with open(json_file, 'r', encoding='utf-8') as f:
            json_content = f.read()

        # Parse JSON first, then validate as DiagramInput
        import json
        try:
            json_data = json.loads(json_content)
        except json.JSONDecodeError:
            # Try with json5 for compatibility
            from ..utils.json_parser import parse_json_string
            json_data = parse_json_string(json_content)

        diagram = DiagramInput.model_validate(json_data)

        logger.info(f"Successfully loaded diagram from file: {json_file.name}")
        logger.info(f"  Title: {diagram.title}")
        logger.info(f"  Elements: {len(diagram.elements)}")
        logger.info(f"  Relationships: {len(diagram.relationships)}")

        # Call the actual diagram creation function directly
        return create_archimate_diagram_impl(diagram)

    except FileNotFoundError as e:
        return f"❌ Error: File not found: {file_path}\n\nDetails: {str(e)}"
    except Exception as e:
        logger.error(f"Error loading diagram from file: {e}")
        return f"❌ Error loading diagram from file:\n\n{str(e)}"
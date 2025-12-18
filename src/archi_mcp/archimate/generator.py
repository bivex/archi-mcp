"""PlantUML ArchiMate diagram generator."""

from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field
import json

from .elements.base import ArchiMateElement
from .relationships import ArchiMateRelationship
from .themes import DiagramStyling, DiagramTheme, PlantUMLSkinParams
from ..utils.exceptions import ArchiMateError, ArchiMateGenerationError
from ..i18n import ArchiMateTranslator


class PlantUMLJSONObject(BaseModel):
    """PlantUML JSON object for displaying data in diagrams."""
    name: str = Field(..., description="JSON object name/identifier")
    data: Union[Dict[str, Any], List[Any]] = Field(..., description="JSON data structure")

    def to_plantuml(self) -> str:
        """Generate PlantUML JSON syntax."""
        json_str = json.dumps(self.data, indent=2, ensure_ascii=False)
        return f"json {self.name} {{\n{json_str}\n}}"


class DiagramLayout(BaseModel):
    """Diagram layout configuration."""
    direction: str = "horizontal"  # horizontal, vertical, layered
    show_legend: bool = True
    show_title: bool = True
    group_by_layer: bool = False
    spacing: str = "normal"  # compact, normal, wide
    show_element_types: bool = False  # show element type names (e.g. Business_Actor)
    show_relationship_labels: bool = True  # show relationship labels and custom names
    theme: DiagramTheme = DiagramTheme.MODERN  # visual theme
    component_style: str = "uml2"  # uml1, uml2, rectangle
    show_component_icons: bool = True  # show ArchiMate icons
    enable_styling: bool = True  # enable enhanced visual styling
    show_documentation: bool = False  # show element documentation as notes
    use_arrow_styles: bool = False  # use new arrow style format for relationships

    # Advanced layout controls
    layout_engine: str = "default"  # default, sfdp, dot, neato, fdp, twopi, circo
    rankdir: str = "TB"  # TB (top-bottom), BT (bottom-top), LR (left-right), RL (right-left)
    concentrate: bool = False  # merge multiple edges
    splines: str = "ortho"  # ortho, curved, line, polyline, spline
    overlap: str = "prism"  # prism, voronoi, scalexy, compress, false
    nodesep: float = 0.25  # minimum separation between nodes
    ranksep: float = 0.5  # minimum separation between ranks

    # Hierarchical grouping
    enable_hierarchical_grouping: bool = False
    grouping_depth: int = 1  # how many levels to group
    group_by_aspect: bool = False  # group by ArchiMate aspects too
    show_empty_groups: bool = False  # show groups even if empty


class ArchiMateGenerator:
    """Generator for PlantUML ArchiMate diagrams."""

    def __init__(self, translator: Optional[ArchiMateTranslator] = None):
        """Initialize the ArchiMate generator.

        Args:
            translator: Optional translator for multilingual support
        """
        self.elements: Dict[str, ArchiMateElement] = {}
        self.relationships: List[ArchiMateRelationship] = []
        self.json_objects: List[PlantUMLJSONObject] = []
        self.hidden_elements: set = set()  # Elements to hide by ID
        self.removed_elements: set = set()  # Elements to remove by ID
        self.hidden_tags: set = set()  # Tags to hide (e.g., $tag)
        self.removed_tags: set = set()  # Tags to remove (e.g., $tag)
        self.layout: DiagramLayout = DiagramLayout()
        self.styling: DiagramStyling = PlantUMLSkinParams.get_theme_presets()[DiagramTheme.MODERN]
        self.translator = translator or ArchiMateTranslator("en")
        
    def add_element(self, element: ArchiMateElement) -> None:
        """Add an ArchiMate element to the diagram.
        
        Args:
            element: ArchiMateElement to add
            
        Raises:
            ArchiMateGenerationError: If element ID already exists
        """
        if element.id in self.elements:
            raise ArchiMateGenerationError(
                f"Element with ID '{element.id}' already exists",
                details={"existing_element": str(self.elements[element.id])}
            )
        
        self.elements[element.id] = element
    
    def add_relationship(self, relationship: ArchiMateRelationship) -> None:
        """Add an ArchiMate relationship to the diagram.
        
        Args:
            relationship: ArchiMateRelationship to add
            
        Raises:
            ArchiMateGenerationError: If relationship validation fails
        """
        # Validate relationship
        errors = relationship.validate_relationship(self.elements)
        if errors:
            raise ArchiMateGenerationError(
                f"Relationship validation failed: {'; '.join(errors)}",
                details={"relationship": str(relationship), "errors": errors}
            )
        
        self.relationships.append(relationship)

    def add_json_object(self, json_obj: PlantUMLJSONObject) -> None:
        """Add a JSON object to display in the diagram.

        Args:
            json_obj: PlantUMLJSONObject to add
        """
        self.json_objects.append(json_obj)

    def hide_elements(self, element_ids: List[str]) -> None:
        """Hide specific elements by ID.

        Args:
            element_ids: List of element IDs to hide
        """
        self.hidden_elements.update(element_ids)

    def remove_elements(self, element_ids: List[str]) -> None:
        """Remove specific elements by ID.

        Args:
            element_ids: List of element IDs to remove
        """
        self.removed_elements.update(element_ids)

    def hide_tags(self, tags: List[str]) -> None:
        """Hide elements with specific tags.

        Args:
            tags: List of tags to hide (e.g., ['$tag1', '$tag2'])
        """
        self.hidden_tags.update(tags)

    def remove_tags(self, tags: List[str]) -> None:
        """Remove elements with specific tags.

        Args:
            tags: List of tags to remove (e.g., ['$tag1', '$tag2'])
        """
        self.removed_tags.update(tags)

    def restore_elements(self, element_ids: List[str]) -> None:
        """Restore previously hidden/removed elements.

        Args:
            element_ids: List of element IDs to restore
        """
        self.hidden_elements.difference_update(element_ids)
        self.removed_elements.difference_update(element_ids)

    def restore_tags(self, tags: List[str]) -> None:
        """Restore elements with specific tags.

        Args:
            tags: List of tags to restore
        """
        self.hidden_tags.difference_update(tags)
        self.removed_tags.difference_update(tags)

    def set_layout(self, layout: DiagramLayout) -> None:
        """Set diagram layout configuration.

        Args:
            layout: DiagramLayout configuration
        """
        self.layout = layout
        # Update styling when layout changes
        if layout.enable_styling:
            self.styling = PlantUMLSkinParams.get_theme_presets()[layout.theme]

    def set_styling(self, styling: DiagramStyling) -> None:
        """Set diagram styling configuration.

        Args:
            styling: DiagramStyling configuration
        """
        self.styling = styling
    
    def generate_plantuml(
        self,
        title: Optional[str] = None,
        description: Optional[str] = None
    ) -> str:
        """Generate complete PlantUML ArchiMate diagram code.

        Args:
            title: Optional diagram title
            description: Optional diagram description

        Returns:
            Complete PlantUML code string

        Raises:
            ArchiMateGenerationError: If generation fails
        """
        if not self.elements:
            raise ArchiMateGenerationError("No elements defined for diagram generation")

        # Update styling based on current layout theme
        if self.layout.enable_styling:
            self.styling = PlantUMLSkinParams.get_theme_presets()[self.layout.theme]

        # Start building PlantUML code
        lines = []

        # Add PlantUML header with UTF-8 encoding pragma
        lines.append("@startuml")
        lines.append("!pragma charset UTF-8")
        lines.append("!include <archimate/Archimate>")

        # Add allowmixing if JSON objects are present
        if self.json_objects:
            lines.append("allowmixing")

        lines.append("")

        # Add enhanced styling if enabled
        if self.layout.enable_styling:
            skinparams = PlantUMLSkinParams.generate_skinparams(self.styling)
            lines.extend(skinparams)
            lines.append("")

        # Component style configuration
        if self.layout.component_style == "uml1":
            lines.append("skinparam componentStyle uml1")
        elif self.layout.component_style == "rectangle":
            lines.append("skinparam componentStyle rectangle")
        else:  # uml2 (default)
            lines.append("skinparam componentStyle uml2")

        lines.append("")

        # Add sprite definitions from all elements
        sprites = self._collect_sprites()
        if sprites:
            sprite_lines = self._generate_sprites(sprites)
            lines.extend(sprite_lines)
            lines.append("")

        # Add title if provided
        if title and self.layout.show_title:
            lines.append(f"title {title}")
            lines.append("")

        # Add description if provided
        if description:
            lines.append(f"' Description: {description}")
            lines.append("")

        # Set direction and advanced layout options
        if self.layout.direction == "vertical":
            lines.append("top to bottom direction")
        elif self.layout.direction == "horizontal":
            lines.append("left to right direction")

        # Add advanced layout controls
        if self.layout.layout_engine != "default":
            lines.append(f"!pragma layout {self.layout.layout_engine}")

        if self.layout.concentrate:
            lines.append("skinparam concentrate true")

        if self.layout.nodesep != 0.25:
            lines.append(f"skinparam nodesep {self.layout.nodesep}")

        if self.layout.ranksep != 0.5:
            lines.append(f"skinparam ranksep {self.layout.ranksep}")

        lines.append("")
        
        # Generate elements - use layout setting for grouping
        if self.layout.group_by_layer:
            self._generate_elements_by_layer(lines)
        else:
            self._generate_elements_sequential(lines)
        
        lines.append("")
        
        # Generate relationships
        self._generate_relationships(lines)

        # Generate JSON objects if any
        if self.json_objects:
            lines.append("")
            self._generate_json_objects(lines)

        # Add legend if requested
        if self.layout.show_legend:
            lines.append("")
            self._generate_legend(lines)
        
        # End PlantUML
        lines.append("")
        lines.append("@enduml")
        
        return "\n".join(lines)
    
    def _generate_elements_sequential(self, lines: List[str]) -> None:
        """Generate elements in sequential order."""
        lines.append("' Elements")
        for element in self.elements.values():
            if self._should_include_element(element):
                plantuml_code = element.to_plantuml(show_element_type=self.layout.show_element_types)
                lines.extend(plantuml_code.split('\n'))

                # Add hide command if element should be hidden
                if self._should_hide_element(element):
                    lines.append(f"hide {element.id}")
    
    def _generate_elements_by_layer(self, lines: List[str]) -> None:
        """Generate elements grouped by layer with advanced hierarchical grouping."""
        # Group elements by layer and optionally by aspect
        layers = {}
        for element in self.elements.values():
            layer = element.layer.value
            if layer not in layers:
                layers[layer] = []
            layers[layer].append(element)

        # Apply hierarchical grouping if enabled
        if self.layout.enable_hierarchical_grouping and self.layout.grouping_depth > 0:
            self._generate_hierarchical_grouping(lines, layers)
        else:
            self._generate_simple_layer_grouping(lines, layers)

    def _generate_simple_layer_grouping(self, lines: List[str], layers: Dict[str, List]) -> None:
        """Generate simple layer-based grouping."""
        # Generate each layer with grouping for multi-layer diagrams
        if len(layers) > 1:
            for layer_name, layer_elements in layers.items():
                translated_layer = self.translator.translate_layer(layer_name)
                lines.append(f"package \"{translated_layer}\" {{")
                for element in layer_elements:
                    if self._should_include_element(element):
                        plantuml_code = element.to_plantuml(show_element_type=self.layout.show_element_types, show_documentation=self.layout.show_documentation)
                        for line in plantuml_code.split('\n'):
                            lines.append("  " + line)

                        # Add hide command if element should be hidden
                        if self._should_hide_element(element):
                            lines.append(f"  hide {element.id}")
                lines.append("}")
                lines.append("")
        else:
            # Single layer - no grouping needed
            for layer_name, layer_elements in layers.items():
                translated_layer = self.translator.translate_layer(layer_name)
                lines.append(f"' {translated_layer}")
                for element in layer_elements:
                    if self._should_include_element(element):
                        plantuml_code = element.to_plantuml(show_element_type=self.layout.show_element_types, show_documentation=self.layout.show_documentation)
                        lines.extend(plantuml_code.split('\n'))

                        # Add hide command if element should be hidden
                        if self._should_hide_element(element):
                            lines.append(f"hide {element.id}")
                lines.append("")

    def _generate_hierarchical_grouping(self, lines: List[str], layers: Dict[str, List]) -> None:
        """Generate hierarchical grouping by layer and aspect."""
        # First group by layer
        for layer_name, layer_elements in layers.items():
            translated_layer = self.translator.translate_layer(layer_name)
            lines.append(f"package \"{translated_layer}\" {{")
            lines.append("")

            if self.layout.group_by_aspect:
                # Group within layer by aspect
                aspects = {}
                for element in layer_elements:
                    aspect = element.aspect.value
                    if aspect not in aspects:
                        aspects[aspect] = []
                    aspects[aspect].append(element)

                for aspect_name, aspect_elements in aspects.items():
                    if len(aspect_elements) > 0 or self.layout.show_empty_groups:
                        translated_aspect = self.translator.translate_aspect(aspect_name)
                        lines.append(f"  package \"{translated_aspect}\" {{")
                        for element in aspect_elements:
                            plantuml_code = element.to_plantuml(show_element_type=self.layout.show_element_types, show_documentation=self.layout.show_documentation)
                            for line in plantuml_code.split('\n'):
                                lines.append("    " + line)
                        lines.append("  }")
                        lines.append("")

            else:
                # Just layer grouping
                for element in layer_elements:
                    if self._should_include_element(element):
                        plantuml_code = element.to_plantuml(show_element_type=self.layout.show_element_types, show_documentation=self.layout.show_documentation)
                        for line in plantuml_code.split('\n'):
                            lines.append("  " + line)

                        # Add hide command if element should be hidden
                        if self._should_hide_element(element):
                            lines.append(f"  hide {element.id}")

            lines.append("}")
            lines.append("")
    
    def _generate_relationships(self, lines: List[str]) -> None:
        """Generate relationships."""
        if not self.relationships:
            return

        lines.append("' Relationships")
        for relationship in self.relationships:
            lines.append(relationship.to_plantuml(
                self.translator,
                show_labels=self.layout.show_relationship_labels,
                use_arrow_styles=self.layout.use_arrow_styles
            ))

    def _generate_json_objects(self, lines: List[str]) -> None:
        """Generate JSON objects for display in diagram."""
        lines.append("' JSON Data Objects")
        for json_obj in self.json_objects:
            lines.append(json_obj.to_plantuml())

    def _should_include_element(self, element: ArchiMateElement) -> bool:
        """Check if an element should be included in the diagram based on hide/remove rules."""
        # Check if element is explicitly removed
        if element.id in self.removed_elements:
            return False

        # Check if element name starts with $ and has no alias (special PlantUML rule)
        if element.name.startswith('$') and element.id == element.name:
            return False

        # Check if element has tags that are removed
        if any(tag in self.removed_tags for tag in element.tags):
            return False

        # Check if element is hidden (but still included, just not visible)
        # Hidden elements are still generated but marked as hidden
        return True

    def _should_hide_element(self, element: ArchiMateElement) -> bool:
        """Check if an element should be hidden (but still included in PlantUML)."""
        # Check if element is explicitly hidden
        if element.id in self.hidden_elements:
            return True

        # Check if element has tags that are hidden
        if any(tag in self.hidden_tags for tag in element.tags):
            return True

        return False
    
    def _generate_legend(self, lines: List[str]) -> None:
        """Generate diagram legend."""
        lines.append("' Legend")
        lines.append("legend right")
        
        # Show layers present in diagram
        layers_used = set(element.layer.value for element in self.elements.values())
        for layer in sorted(layers_used):
            translated_layer = self.translator.translate_layer(layer)
            lines.append(f"  {translated_layer}")
        
        lines.append("end legend")
    
    def clear(self) -> None:
        """Clear all elements, relationships, JSON objects, and hide/remove rules."""
        self.elements.clear()
        self.relationships.clear()
        self.json_objects.clear()
        self.hidden_elements.clear()
        self.removed_elements.clear()
        self.hidden_tags.clear()
        self.removed_tags.clear()
    
    def get_element_count(self) -> int:
        """Get number of elements in diagram."""
        return len(self.elements)
    
    def get_relationship_count(self) -> int:
        """Get number of relationships in diagram."""
        return len(self.relationships)
    
    def get_layers_used(self) -> List[str]:
        """Get list of layers used in diagram."""
        return list(set(element.layer.value for element in self.elements.values()))
    
    def _collect_sprites(self) -> List['PlantUMLSprite']:
        """Collect all sprites from elements in the diagram."""
        from .elements.base import PlantUMLSprite
        sprites = []
        seen_names = set()

        for element in self.elements.values():
            for sprite in element.sprites:
                if sprite.name not in seen_names:
                    sprites.append(sprite)
                    seen_names.add(sprite.name)

        return sprites

    def _generate_sprites(self, sprites: List['PlantUMLSprite']) -> List[str]:
        """Generate PlantUML sprite definitions."""
        lines = []
        for sprite in sprites:
            lines.append(sprite.to_plantuml())
        return lines

    def validate_diagram(self) -> List[str]:
        """Validate the complete diagram.

        Returns:
            List of validation errors (empty if valid)
        """
        errors = []

        # Validate all elements
        for element in self.elements.values():
            element_errors = element.validate_element()
            if element_errors:
                errors.extend([f"Element {element.id}: {error}" for error in element_errors])

        # Validate all relationships
        for relationship in self.relationships:
            rel_errors = relationship.validate_relationship(self.elements)
            if rel_errors:
                errors.extend([f"Relationship {relationship.id}: {error}" for error in rel_errors])

        return errors
    
    def export_to_file(self, filepath: str, title: Optional[str] = None) -> None:
        """Export diagram to PlantUML file.
        
        Args:
            filepath: Output file path
            title: Optional diagram title
            
        Raises:
            ArchiMateError: If export fails
        """
        try:
            plantuml_code = self.generate_plantuml(title=title)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(plantuml_code)
        except Exception as e:
            raise ArchiMateGenerationError(
                f"Failed to export diagram to file: {str(e)}",
                details={"filepath": filepath, "error": str(e)}
            )
    
    def generate_png_to_tmp(self, title: Optional[str] = None) -> str:
        """Generate PNG image to /tmp directory and return file path.
        
        Args:
            title: Optional diagram title for filename
            
        Returns:
            File path to generated PNG image
            
        Raises:
            ArchiMateError: If PNG generation fails
        """
        import tempfile
        import subprocess
        import os
        import time
        from pathlib import Path
        
        try:
            # Generate PlantUML code
            plantuml_code = self.generate_plantuml(title=title)
            
            # Create temporary PlantUML file
            timestamp = int(time.time())
            temp_filename = f"archimate_diagram_{timestamp}"
            if title:
                # Clean title for filename
                clean_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
                clean_title = clean_title.replace(' ', '_')[:50]  # Limit length
                temp_filename = f"archimate_{clean_title}_{timestamp}"
            
            temp_puml_path = f"/tmp/{temp_filename}.puml"
            temp_png_path = f"/tmp/{temp_filename}.png"
            
            # Write PlantUML code
            with open(temp_puml_path, 'w', encoding='utf-8') as f:
                f.write(plantuml_code)
            
            # Find PlantUML jar
            possible_jars = [
                "/Users/patrik/Projects/archi-mcp/plantuml.jar",
                "./plantuml.jar",
                "/usr/local/bin/plantuml.jar",
                "/opt/homebrew/bin/plantuml.jar"
            ]
            
            plantuml_jar = None
            for jar_path in possible_jars:
                if os.path.exists(jar_path):
                    plantuml_jar = jar_path
                    break
            
            if not plantuml_jar:
                error_msg = """PlantUML jar not found. Download it by running:
curl -L https://github.com/plantuml/plantuml/releases/latest/download/plantuml.jar -o plantuml.jar

The jar should be placed in the project root directory or one of these locations:
- ./plantuml.jar (current directory)
- /usr/local/bin/plantuml.jar
- /opt/homebrew/bin/plantuml.jar"""
                raise ArchiMateGenerationError(error_msg)
            
            # Generate PNG (with headless mode to prevent focus stealing)
            cmd = ["java", "-Djava.awt.headless=true", "-jar", plantuml_jar, "-tpng", temp_puml_path]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode != 0:
                raise ArchiMateGenerationError(f"PlantUML generation failed: {result.stderr}")
            
            # Verify PNG was created
            if not os.path.exists(temp_png_path):
                raise ArchiMateGenerationError("PNG file was not generated")
            
            # Clean up temporary PlantUML file
            try:
                os.unlink(temp_puml_path)
            except:
                pass  # Don't fail if cleanup fails
            
            return temp_png_path
            
        except subprocess.TimeoutExpired:
            raise ArchiMateGenerationError("PlantUML generation timed out")
        except Exception as e:
            raise ArchiMateGenerationError(f"Failed to generate PNG: {str(e)}")
    

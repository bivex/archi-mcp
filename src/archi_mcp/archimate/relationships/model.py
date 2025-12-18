"""ArchiMate relationship model definitions."""

from enum import Enum
from typing import List, Optional, Dict
from pydantic import BaseModel, Field

from ...utils.exceptions import ArchiMateRelationshipError
from .types import ArchiMateRelationshipType


class RelationshipDirection(str, Enum):
    """Relationship direction modifiers for PlantUML."""
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"
    UP_LEFT = "up-left"
    UP_RIGHT = "up-right"
    DOWN_LEFT = "down-left"
    DOWN_RIGHT = "down-right"


class ArrowStyle(str, Enum):
    """Arrow style variations for relationships."""
    SOLID = "-->"  # solid arrow
    DASHED = "..>"  # dashed arrow (dependency)
    SOLID_REVERSE = "<--"  # reverse solid
    DASHED_REVERSE = "<.."  # reverse dashed
    BIDIRECTIONAL = "<-->"  # bidirectional
    COMPOSITION = "*-->"  # composition (filled diamond)
    AGGREGATION = "o-->"  # aggregation (empty diamond)
    ASSIGNMENT = "--*"  # assignment (to filled diamond)
    ASSIGNMENT_REVERSE = "*--"  # assignment (from filled diamond)
    SERVING = "--("  # serving (to circle)
    SERVING_REVERSE = ")--"  # serving (from circle)
    ACCESS_READ = "-->>"  # access read
    ACCESS_WRITE = "<<--"  # access write
    ACCESS_READ_WRITE = "<<-->>"  # access read/write
    INFLUENCE = "..>>"  # influence
    FLOW = "~>"  # flow
    TRIGGERING = "->>"  # triggering
    SPECIALIZATION = "--|>"  # specialization
    REALIZATION = "..|>"  # realization


# Relationship type to arrow style mapping
RELATIONSHIP_ARROW_STYLES: Dict[ArchiMateRelationshipType, ArrowStyle] = {
    ArchiMateRelationshipType.ASSIGNMENT: ArrowStyle.ASSIGNMENT,
    ArchiMateRelationshipType.AGGREGATION: ArrowStyle.AGGREGATION,
    ArchiMateRelationshipType.COMPOSITION: ArrowStyle.COMPOSITION,
    ArchiMateRelationshipType.SERVING: ArrowStyle.SERVING,
    ArchiMateRelationshipType.ACCESS: ArrowStyle.ACCESS_READ,
    ArchiMateRelationshipType.INFLUENCE: ArrowStyle.INFLUENCE,
    ArchiMateRelationshipType.FLOW: ArrowStyle.FLOW,
    ArchiMateRelationshipType.TRIGGERING: ArrowStyle.TRIGGERING,
    ArchiMateRelationshipType.SPECIALIZATION: ArrowStyle.SPECIALIZATION,
    ArchiMateRelationshipType.REALIZATION: ArrowStyle.REALIZATION,
    ArchiMateRelationshipType.ASSOCIATION: ArrowStyle.SOLID,
}


class ArchiMateRelationship(BaseModel):
    """ArchiMate relationship definition."""

    id: str = Field(..., description="Unique identifier for the relationship")
    from_element: str = Field(..., description="Source element ID")
    to_element: str = Field(..., description="Target element ID")
    relationship_type: ArchiMateRelationshipType = Field(..., description="Type of relationship")
    direction: Optional[RelationshipDirection] = Field(None, description="Optional direction")
    arrow_style: Optional[ArrowStyle] = Field(None, description="Custom arrow style override")
    line_style: str = Field("solid", description="Line style: solid, dashed, dotted")
    color: Optional[str] = Field(None, description="Custom color for this relationship")
    description: Optional[str] = Field(None, description="Relationship description")
    label: Optional[str] = Field(None, description="Relationship label")
    length: Optional[int] = Field(None, description="Arrow length modifier (1-5)")
    positioning: Optional[str] = Field(None, description="Advanced positioning hints (e.g., 'hidden' for invisible layout relationships)")
    orientation: str = Field("vertical", description="Arrow orientation: vertical (default --), horizontal (-), or dot (.)")
    properties: dict = Field(default_factory=dict, description="Additional properties")

    def get_default_arrow_style(self) -> ArrowStyle:
        """Get default arrow style for this relationship type."""
        return RELATIONSHIP_ARROW_STYLES.get(self.relationship_type, ArrowStyle.SOLID)

    def get_arrow_style(self) -> ArrowStyle:
        """Get arrow style, using custom override if specified."""
        return self.arrow_style or self.get_default_arrow_style()

    def to_plantuml(self, translator=None, show_labels: bool = True, use_arrow_styles: bool = False) -> str:
        """Generate PlantUML code for this relationship.

        Args:
            translator: Optional translator for relationship labels
            show_labels: Whether to display relationship labels and custom names
            use_arrow_styles: Whether to use new arrow style format (for backward compatibility)

        Returns:
            PlantUML relationship code
        """
        # Determine arrow style
        arrow_style = self.arrow_style
        if not arrow_style:
            # Use default style based on relationship type
            arrow_style = RELATIONSHIP_ARROW_STYLES.get(self.relationship_type, ArrowStyle.SOLID)

        # Start with the arrow style value as a string for modifications
        final_arrow = arrow_style.value

        # Apply orientation modifications
        if self.orientation == "horizontal":
            # Convert vertical arrows (--) to horizontal (-)
            final_arrow = final_arrow.replace("--", "-")
        elif self.orientation == "dot":
            # Convert to dot notation
            final_arrow = final_arrow.replace("-->", ".").replace("--", ".").replace("..", ".").replace("~>", ".>")

        # Apply line style modifications
        if self.line_style == "dashed":
            # Convert solid arrows to dashed
            final_arrow = final_arrow.replace("--", "..")
        elif self.line_style == "dotted":
            # Convert to dotted (using PlantUML dotted syntax)
            final_arrow = final_arrow.replace("--", "-.").replace("..", "-.")

        # Handle direction modifications
        if self.direction:
            # Apply directional hints with precise PlantUML syntax support
            direction_map = {
                RelationshipDirection.UP: "up",
                RelationshipDirection.DOWN: "down",
                RelationshipDirection.LEFT: "left",
                RelationshipDirection.RIGHT: "right",
                RelationshipDirection.UP_LEFT: "up-left",
                RelationshipDirection.UP_RIGHT: "up-right",
                RelationshipDirection.DOWN_LEFT: "down-left",
                RelationshipDirection.DOWN_RIGHT: "down-right"
            }

            direction = direction_map.get(self.direction)
            if direction:
                # Apply direction to arrow components precisely, avoiding duplication
                # Split arrow into components and apply direction to each applicable part

                # Handle bidirectional arrows (<<-->>)
                if "<<-->>" in final_arrow:
                    final_arrow = final_arrow.replace("<<-->>", f"<<{direction}-{direction}>>")
                elif "<<->>" in final_arrow:
                    final_arrow = final_arrow.replace("<<->>", f"<<{direction}-{direction}>>")

                # Handle bidirectional solid arrows (<-->)
                elif "<-->" in final_arrow:
                    final_arrow = final_arrow.replace("<-->", f"<{direction}-{direction}>")
                elif "<->" in final_arrow:
                    final_arrow = final_arrow.replace("<->", f"<{direction}-{direction}>")

                # Handle access read arrows (-->>)
                elif "-->>" in final_arrow:
                    final_arrow = final_arrow.replace("-->>", f"-{direction}->>")
                elif "->>" in final_arrow:
                    final_arrow = final_arrow.replace("->>", f"-{direction}>>")

                # Handle influence arrows (..>>)
                elif "..>>" in final_arrow:
                    final_arrow = final_arrow.replace("..>>", f".{direction}.>>")
                elif ".>>" in final_arrow:
                    final_arrow = final_arrow.replace(".>>", f".{direction}.>>")

                # Handle specialization arrows (--|>)
                elif "--|>" in final_arrow:
                    final_arrow = final_arrow.replace("--|>", f"-{direction}-|>")
                elif "-|>" in final_arrow:
                    final_arrow = final_arrow.replace("-|>", f"-{direction}-|>")

                # Handle realization arrows (..|>)
                elif "..|>" in final_arrow:
                    final_arrow = final_arrow.replace("..|>", f".{direction}.|>")
                elif ".|>" in final_arrow:
                    final_arrow = final_arrow.replace(".|>", f".{direction}.|>")

                # Handle serving arrows (--()
                elif "--(" in final_arrow:
                    final_arrow = final_arrow.replace("--(", f"-{direction}-(")
                elif "-(" in final_arrow:
                    final_arrow = final_arrow.replace("-(", f"-{direction}-(")

                # Handle reverse serving arrows )--
                elif ")--" in final_arrow:
                    final_arrow = final_arrow.replace(")--", f")-{direction}-")
                elif ")-" in final_arrow:
                    final_arrow = final_arrow.replace(")-", f")-{direction}-")

                # Handle access write arrows (<<--)
                elif "<<--" in final_arrow:
                    final_arrow = final_arrow.replace("<<--", f"<<{direction}-")
                elif "<<-" in final_arrow:
                    final_arrow = final_arrow.replace("<<-", f"<<{direction}-")

                # Handle composition arrows (*-->)
                elif "*-->" in final_arrow:
                    final_arrow = final_arrow.replace("*-->", f"*-{direction}->")
                elif "*->" in final_arrow:
                    final_arrow = final_arrow.replace("*->", f"*-{direction}->")

                # Handle aggregation arrows (o-->)
                elif "o-->" in final_arrow:
                    final_arrow = final_arrow.replace("o-->", f"o-{direction}->")
                elif "o->" in final_arrow:
                    final_arrow = final_arrow.replace("o->", f"o-{direction}->")

                # Handle assignment arrows (--*)
                elif "--*" in final_arrow:
                    final_arrow = final_arrow.replace("--*", f"-{direction}-*")
                elif "-*" in final_arrow:
                    final_arrow = final_arrow.replace("-*", f"-{direction}-*")

                # Handle reverse assignment arrows (*--)
                elif "*--" in final_arrow:
                    final_arrow = final_arrow.replace("*--", f"*-{direction}-")
                elif "*-" in final_arrow:
                    final_arrow = final_arrow.replace("*-", f"*-{direction}-")

                # Handle reverse solid arrows (<--)
                elif "<--" in final_arrow:
                    final_arrow = final_arrow.replace("<--", f"<{direction}-")
                elif "<-" in final_arrow:
                    final_arrow = final_arrow.replace("<-", f"<{direction}-")

                # Handle reverse dashed arrows (<..)
                elif "<.." in final_arrow:
                    final_arrow = final_arrow.replace("<..", f"<{direction}.")
                elif "<." in final_arrow:
                    final_arrow = final_arrow.replace("<.", f"<{direction}.")

                # Handle standard solid arrows (-->)
                elif "-->" in final_arrow:
                    final_arrow = final_arrow.replace("-->", f"-{direction}->")

                # Handle standard dashed arrows (..>)
                elif "..>" in final_arrow:
                    final_arrow = final_arrow.replace("..>", f".{direction}.>")

                # Handle flow arrows (~>)
                elif "~>" in final_arrow:
                    final_arrow = final_arrow.replace("~>", f"~{direction}>")

        # Determine relationship label
        label = ""
        if show_labels:
            if self.label:
                label = f" : {self.label}"
            elif translator:
                # Use translated relationship type as fallback
                translated_type = translator.translate_relationship(self.relationship_type.value)
                label = f" : {translated_type}"

        # Add color if specified
        color_str = ""
        if self.color:
            color_str = f" {self.color}"

        # Add length modifier if specified
        length_str = ""
        if self.length and 1 <= self.length <= 5:
            length_str = str(self.length)

        # Handle positioning options
        positioning_prefix = ""
        positioning_suffix = ""
        if self.positioning == "hidden":
            positioning_prefix = "hidden "
        elif self.positioning:
            # Other positioning hints can be added here
            pass

        if use_arrow_styles:
            # New format with arrow styles
            plantuml_code = f'{positioning_prefix}"{self.from_element}" {final_arrow}{length_str} "{self.to_element}"{color_str}{label}{positioning_suffix}'
        else:
            # Legacy format for backward compatibility
            rel_type = self.relationship_type.value

            if show_labels:
                if self.label:
                    legacy_label = f'"{self.label}"'
                elif self.description:
                    legacy_label = f'"{self.description}"'
                elif translator:
                    translated_rel = translator.translate_relationship(self.relationship_type.value)
                    legacy_label = f'"{translated_rel}"'
                else:
                    legacy_label = f'"{rel_type.lower()}"'
            else:
                legacy_label = '""'

            plantuml_code = f'{positioning_prefix}Rel_{rel_type}({self.from_element}, {self.to_element}, {legacy_label}){positioning_suffix}'

        return plantuml_code

    def validate_relationship(self, elements: dict) -> List[str]:
        """Validate the relationship according to ArchiMate specification.

        Args:
            elements: Dictionary of element IDs to ArchiMateElement objects

        Returns:
            List of validation errors (empty if valid)
        """
        errors = []

        # Check required fields
        if not self.id:
            errors.append("Relationship ID is required")
        if not self.from_element:
            errors.append("Source element ID is required")
        if not self.to_element:
            errors.append("Target element ID is required")
        if not self.relationship_type:
            errors.append("Relationship type is required")

        # Check for self-references
        if self.from_element == self.to_element:
            errors.append("Relationship cannot reference the same element")

        # Check if referenced elements exist
        if self.from_element not in elements:
            errors.append(f"Source element '{self.from_element}' does not exist")
        if self.to_element not in elements:
            errors.append(f"Target element '{self.to_element}' does not exist")

        # If elements exist, perform additional validation
        if self.from_element in elements and self.to_element in elements:
            from_elem = elements[self.from_element]
            to_elem = elements[self.to_element]

            # Validate relationship constraints based on element types and layers
            constraint_errors = self._validate_relationship_constraints(from_elem, to_elem)
            errors.extend(constraint_errors)

        return errors

    def _validate_relationship_constraints(self, from_elem, to_elem) -> List[str]:
        """Validate relationship constraints between source and target elements.

        Args:
            from_elem: Source ArchiMateElement
            to_elem: Target ArchiMateElement

        Returns:
            List of constraint validation errors
        """
        errors = []

        # Basic layer compatibility check
        if hasattr(from_elem, 'layer') and hasattr(to_elem, 'layer'):
            # Allow relationships within the same layer or between compatible layers
            compatible_layers = {
                'Business': ['Business', 'Application', 'Technology', 'Physical', 'Implementation', 'Motivation', 'Strategy'],
                'Application': ['Business', 'Application', 'Technology', 'Physical', 'Implementation', 'Motivation', 'Strategy'],
                'Technology': ['Business', 'Application', 'Technology', 'Physical', 'Implementation', 'Motivation', 'Strategy'],
                'Physical': ['Business', 'Application', 'Technology', 'Physical', 'Implementation', 'Motivation', 'Strategy'],
                'Implementation': ['Business', 'Application', 'Technology', 'Physical', 'Implementation', 'Motivation', 'Strategy'],
                'Motivation': ['Business', 'Application', 'Technology', 'Physical', 'Implementation', 'Motivation', 'Strategy'],
                'Strategy': ['Business', 'Application', 'Technology', 'Physical', 'Implementation', 'Motivation', 'Strategy']
            }

            from_layer = str(from_elem.layer.value) if hasattr(from_elem.layer, 'value') else str(from_elem.layer)
            to_layer = str(to_elem.layer.value) if hasattr(to_elem.layer, 'value') else str(to_elem.layer)

            if to_layer not in compatible_layers.get(from_layer, []):
                errors.append(f"Invalid relationship from {from_layer} layer to {to_layer} layer")

        return errors

    def __str__(self) -> str:
        return f"{self.from_element} --{self.relationship_type.value}--> {self.to_element}"


# Relationship type mapping for backward compatibility
ARCHIMATE_RELATIONSHIPS = {
    "Access": ArchiMateRelationshipType.ACCESS,
    "Aggregation": ArchiMateRelationshipType.AGGREGATION,
    "Assignment": ArchiMateRelationshipType.ASSIGNMENT,
    "Association": ArchiMateRelationshipType.ASSOCIATION,
    "Composition": ArchiMateRelationshipType.COMPOSITION,
    "Flow": ArchiMateRelationshipType.FLOW,
    "Influence": ArchiMateRelationshipType.INFLUENCE,
    "Realization": ArchiMateRelationshipType.REALIZATION,
    "Serving": ArchiMateRelationshipType.SERVING,
    "Specialization": ArchiMateRelationshipType.SPECIALIZATION,
    "Triggering": ArchiMateRelationshipType.TRIGGERING,
}


def create_relationship(
    relationship_id: str,
    from_element: str,
    to_element: str,
    relationship_type: str,
    direction: Optional[str] = None,
    description: Optional[str] = None,
    label: Optional[str] = None,
    **kwargs
) -> ArchiMateRelationship:
    """Create an ArchiMate relationship.

    Args:
        relationship_id: Unique identifier for the relationship
        from_element: Source element ID
        to_element: Target element ID
        relationship_type: Type of relationship
        direction: Optional direction (Up, Down, Left, Right)
        description: Optional description
        label: Optional label
        **kwargs: Additional properties

    Returns:
        ArchiMateRelationship instance

    Raises:
        ArchiMateRelationshipError: If relationship type is invalid
    """
    from ...utils.exceptions import ArchiMateRelationshipError

    # Validate relationship type
    if relationship_type not in ARCHIMATE_RELATIONSHIPS:
        valid_types = list(ARCHIMATE_RELATIONSHIPS.keys())
        raise ArchiMateRelationshipError(
            f"Invalid relationship type '{relationship_type}'. "
            f"Valid types: {valid_types}",
            from_element=from_element,
            to_element=to_element,
            relationship_type=relationship_type
        )

    # Validate direction if provided
    direction_enum = None
    if direction:
        try:
            direction_enum = RelationshipDirection(direction.lower())
        except ValueError:
            valid_directions = [d.value for d in RelationshipDirection]
            raise ArchiMateRelationshipError(
                f"Invalid direction '{direction}'. "
                f"Valid directions: {valid_directions}",
                from_element=from_element,
                to_element=to_element,
                relationship_type=relationship_type
            )

    return ArchiMateRelationship(
        id=relationship_id,
        from_element=from_element,
        to_element=to_element,
        relationship_type=ARCHIMATE_RELATIONSHIPS[relationship_type],
        direction=direction_enum,
        description=description,
        label=label,
        properties=kwargs
    )
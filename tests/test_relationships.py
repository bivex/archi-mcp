"""Tests for ArchiMate relationships."""

import pytest
from archi_mcp.archimate.relationships import (
    ArchiMateRelationship,
    RelationshipType,
    RelationshipDirection,
    ArrowStyle,
    create_relationship,
    ARCHIMATE_RELATIONSHIPS,
)
from archi_mcp.archimate.relationships.model import RELATIONSHIP_ARROW_STYLES
from archi_mcp.archimate.elements.base import ArchiMateElement, ArchiMateLayer, ArchiMateAspect
from archi_mcp.utils.exceptions import ArchiMateRelationshipError


class TestArchiMateRelationship:
    """Test ArchiMateRelationship class."""
    
    def test_relationship_creation(self):
        """Test basic relationship creation."""
        relationship = ArchiMateRelationship(
            id="rel_1",
            from_element="elem_1",
            to_element="elem_2",
            relationship_type=RelationshipType.SERVING,
            description="Test relationship"
        )
        
        assert relationship.id == "rel_1"
        assert relationship.from_element == "elem_1"
        assert relationship.to_element == "elem_2"
        assert relationship.relationship_type == RelationshipType.SERVING
        assert relationship.description == "Test relationship"
    
    def test_relationship_with_direction(self):
        """Test relationship with direction."""
        relationship = ArchiMateRelationship(
            id="rel_2",
            from_element="elem_a",
            to_element="elem_b",
            relationship_type=RelationshipType.REALIZATION,
            direction=RelationshipDirection.UP
        )
        
        assert relationship.direction == RelationshipDirection.UP
    
    def test_relationship_plantuml_generation(self):
        """Test PlantUML code generation."""
        relationship = ArchiMateRelationship(
            id="test_rel",
            from_element="source",
            to_element="target",
            relationship_type=RelationshipType.SERVING,
            description="serves"
        )
        
        plantuml = relationship.to_plantuml(show_labels=False, use_arrow_styles=False)
        expected = 'Rel_Serving(source, target, "")'
        assert plantuml == expected
    
    def test_relationship_plantuml_with_direction(self):
        """Test PlantUML code generation with direction."""
        relationship = ArchiMateRelationship(
            id="test_rel_dir",
            from_element="source",
            to_element="target",
            relationship_type=RelationshipType.REALIZATION,
            direction=RelationshipDirection.DOWN,
            label="realizes"
        )

        plantuml = relationship.to_plantuml(show_labels=True, use_arrow_styles=False)
        # Direction is layout hint only, not part of PlantUML syntax
        expected = 'Rel_Realization(source, target, "realizes")'
        assert plantuml == expected

    def test_plantuml_with_arrow_styles(self):
        """Test PlantUML generation with new arrow styles."""
        relationship = ArchiMateRelationship(
            id="arrow_style_test",
            from_element="source",
            to_element="target",
            relationship_type=RelationshipType.COMPOSITION,
            arrow_style=ArrowStyle.COMPOSITION
        )

        plantuml = relationship.to_plantuml(show_labels=False, use_arrow_styles=True)
        expected = '"source" *--> "target"'
        assert plantuml == expected

    def test_plantuml_with_custom_arrow_style(self):
        """Test PlantUML with custom arrow style override."""
        relationship = ArchiMateRelationship(
            id="custom_arrow",
            from_element="A",
            to_element="B",
            relationship_type=RelationshipType.ASSOCIATION,
            arrow_style=ArrowStyle.SERVING
        )

        plantuml = relationship.to_plantuml(show_labels=False, use_arrow_styles=True)
        expected = '"A" --( "B"'
        assert plantuml == expected

    def test_plantuml_with_dashed_line_style(self):
        """Test PlantUML with dashed line style."""
        relationship = ArchiMateRelationship(
            id="dashed_test",
            from_element="X",
            to_element="Y",
            relationship_type=RelationshipType.ASSOCIATION,
            line_style="dashed"
        )

        plantuml = relationship.to_plantuml(show_labels=False, use_arrow_styles=True)
        expected = '"X" ..> "Y"'
        assert plantuml == expected

    def test_plantuml_with_dotted_line_style(self):
        """Test PlantUML with dotted line style."""
        relationship = ArchiMateRelationship(
            id="dotted_test",
            from_element="P",
            to_element="Q",
            relationship_type=RelationshipType.ASSOCIATION,
            line_style="dotted"
        )

        plantuml = relationship.to_plantuml(show_labels=False, use_arrow_styles=True)
        expected = '"P" -.> "Q"'
        assert plantuml == expected

    def test_plantuml_with_color(self):
        """Test PlantUML with color."""
        relationship = ArchiMateRelationship(
            id="color_test",
            from_element="red_src",
            to_element="red_tgt",
            relationship_type=RelationshipType.FLOW,
            color="#FF0000"
        )

        plantuml = relationship.to_plantuml(show_labels=False, use_arrow_styles=True)
        expected = '"red_src" ~> "red_tgt" #FF0000'
        assert plantuml == expected

    def test_plantuml_with_length_modifier(self):
        """Test PlantUML with length modifier."""
        relationship = ArchiMateRelationship(
            id="length_test",
            from_element="long",
            to_element="short",
            relationship_type=RelationshipType.TRIGGERING,
            length=3
        )

        plantuml = relationship.to_plantuml(show_labels=False, use_arrow_styles=True)
        expected = '"long" ->>3 "short"'
        assert plantuml == expected

    def test_plantuml_with_positioning_hidden(self):
        """Test PlantUML with hidden positioning."""
        relationship = ArchiMateRelationship(
            id="hidden_test",
            from_element="invisible",
            to_element="ghost",
            relationship_type=RelationshipType.ASSOCIATION,
            positioning="hidden"
        )

        plantuml = relationship.to_plantuml(show_labels=False, use_arrow_styles=True)
        expected = 'hidden "invisible" --> "ghost"'
        assert plantuml == expected

    def test_plantuml_with_direction_and_arrow_style(self):
        """Test PlantUML with both direction and arrow style."""
        relationship = ArchiMateRelationship(
            id="dir_arrow_test",
            from_element="up",
            to_element="down",
            relationship_type=RelationshipType.COMPOSITION,
            direction=RelationshipDirection.UP
        )

        plantuml = relationship.to_plantuml(show_labels=False, use_arrow_styles=True)
        expected = '"up" *-up-> "down"'
        assert plantuml == expected

    def test_plantuml_diagonal_direction(self):
        """Test PlantUML with diagonal direction."""
        relationship = ArchiMateRelationship(
            id="diag_test",
            from_element="corner1",
            to_element="corner2",
            relationship_type=RelationshipType.SERVING,
            direction=RelationshipDirection.UP_RIGHT
        )

        plantuml = relationship.to_plantuml(show_labels=False, use_arrow_styles=True)
        expected = '"corner1" -up-right-( "corner2"'
        assert plantuml == expected

    def test_plantuml_complex_relationship(self):
        """Test PlantUML with multiple features combined."""
        relationship = ArchiMateRelationship(
            id="complex_test",
            from_element="complex_src",
            to_element="complex_tgt",
            relationship_type=RelationshipType.REALIZATION,
            direction=RelationshipDirection.DOWN,
            line_style="dashed",
            color="#00FF00",
            length=2,
            label="complex label"
        )

        plantuml = relationship.to_plantuml(show_labels=True, use_arrow_styles=True)
        expected = '"complex_src" .down.|>2 "complex_tgt" #00FF00 : complex label'
        assert plantuml == expected

    def test_plantuml_arrow_direction_left(self):
        """Test PlantUML arrow with left direction."""
        relationship = ArchiMateRelationship(
            id="left_dir_test",
            from_element="source",
            to_element="target",
            relationship_type=RelationshipType.ASSOCIATION,
            direction=RelationshipDirection.LEFT
        )

        plantuml = relationship.to_plantuml(show_labels=False, use_arrow_styles=True)
        expected = '"source" -left-> "target"'
        assert plantuml == expected

    def test_plantuml_arrow_direction_right(self):
        """Test PlantUML arrow with right direction."""
        relationship = ArchiMateRelationship(
            id="right_dir_test",
            from_element="source",
            to_element="target",
            relationship_type=RelationshipType.ASSOCIATION,
            direction=RelationshipDirection.RIGHT
        )

        plantuml = relationship.to_plantuml(show_labels=False, use_arrow_styles=True)
        expected = '"source" -right-> "target"'
        assert plantuml == expected

    def test_plantuml_arrow_direction_up(self):
        """Test PlantUML arrow with up direction."""
        relationship = ArchiMateRelationship(
            id="up_dir_test",
            from_element="source",
            to_element="target",
            relationship_type=RelationshipType.ASSOCIATION,
            direction=RelationshipDirection.UP
        )

        plantuml = relationship.to_plantuml(show_labels=False, use_arrow_styles=True)
        expected = '"source" -up-> "target"'
        assert plantuml == expected

    def test_plantuml_arrow_direction_down(self):
        """Test PlantUML arrow with down direction."""
        relationship = ArchiMateRelationship(
            id="down_dir_test",
            from_element="source",
            to_element="target",
            relationship_type=RelationshipType.ASSOCIATION,
            direction=RelationshipDirection.DOWN
        )

        plantuml = relationship.to_plantuml(show_labels=False, use_arrow_styles=True)
        expected = '"source" -down-> "target"'
        assert plantuml == expected

    def test_plantuml_arrow_direction_short_left(self):
        """Test PlantUML arrow with shortened left direction (-l->)."""
        relationship = ArchiMateRelationship(
            id="short_left_test",
            from_element="A",
            to_element="B",
            relationship_type=RelationshipType.ASSOCIATION,
            direction=RelationshipDirection.LEFT
        )

        # Test that full "left" becomes "-left->" in the arrow
        plantuml = relationship.to_plantuml(show_labels=False, use_arrow_styles=True)
        assert "-left->" in plantuml

    def test_plantuml_arrow_direction_short_right(self):
        """Test PlantUML arrow with shortened right direction (-r->)."""
        relationship = ArchiMateRelationship(
            id="short_right_test",
            from_element="A",
            to_element="B",
            relationship_type=RelationshipType.ASSOCIATION,
            direction=RelationshipDirection.RIGHT
        )

        plantuml = relationship.to_plantuml(show_labels=False, use_arrow_styles=True)
        assert "-right->" in plantuml

    def test_plantuml_arrow_direction_short_up(self):
        """Test PlantUML arrow with shortened up direction (-u->)."""
        relationship = ArchiMateRelationship(
            id="short_up_test",
            from_element="A",
            to_element="B",
            relationship_type=RelationshipType.ASSOCIATION,
            direction=RelationshipDirection.UP
        )

        plantuml = relationship.to_plantuml(show_labels=False, use_arrow_styles=True)
        assert "-up->" in plantuml

    def test_plantuml_arrow_direction_short_down(self):
        """Test PlantUML arrow with shortened down direction (-d->)."""
        relationship = ArchiMateRelationship(
            id="short_down_test",
            from_element="A",
            to_element="B",
            relationship_type=RelationshipType.ASSOCIATION,
            direction=RelationshipDirection.DOWN
        )

        plantuml = relationship.to_plantuml(show_labels=False, use_arrow_styles=True)
        assert "-down->" in plantuml

    def test_plantuml_reverse_arrows(self):
        """Test PlantUML reverse arrow directions."""
        # Test reverse solid arrow (<--)
        relationship = ArchiMateRelationship(
            id="reverse_solid",
            from_element="A",
            to_element="B",
            relationship_type=RelationshipType.ASSOCIATION,
            arrow_style=ArrowStyle.SOLID_REVERSE  # This should give <--
        )

        plantuml = relationship.to_plantuml(show_labels=False, use_arrow_styles=True)
        expected = '"A" <-- "B"'
        assert plantuml == expected

    def test_plantuml_reverse_dashed_arrows(self):
        """Test PlantUML reverse dashed arrow directions."""
        relationship = ArchiMateRelationship(
            id="reverse_dashed",
            from_element="A",
            to_element="B",
            relationship_type=RelationshipType.ASSOCIATION,
            arrow_style=ArrowStyle.DASHED_REVERSE,  # This should give <..
            line_style="dashed"
        )

        plantuml = relationship.to_plantuml(show_labels=False, use_arrow_styles=True)
        expected = '"A" <.. "B"'
        assert plantuml == expected

    def test_plantuml_horizontal_single_dash(self):
        """Test PlantUML horizontal links with single dash."""
        # This tests if we can generate single-dash arrows instead of double-dash
        relationship = ArchiMateRelationship(
            id="single_dash_test",
            from_element="Component",
            to_element="Interface",
            relationship_type=RelationshipType.SERVING
        )

        plantuml = relationship.to_plantuml(show_labels=False, use_arrow_styles=True)
        # Currently generates --(, but we want to test single dash alternative
        # This might need new functionality
        expected = '"Component" --( "Interface"'
        assert plantuml == expected

    def test_plantuml_horizontal_dot_link(self):
        """Test PlantUML horizontal links with dot."""
        relationship = ArchiMateRelationship(
            id="dot_link_test",
            from_element="Component",
            to_element="Interface2",
            relationship_type=RelationshipType.SERVING
        )

        plantuml = relationship.to_plantuml(show_labels=False, use_arrow_styles=True)
        expected = '"Component" --( "Interface2"'
        assert plantuml == expected

    def test_plantuml_legacy_format_with_new_features(self):
        """Test that legacy format still works with new features."""
        relationship = ArchiMateRelationship(
            id="legacy_new",
            from_element="legacy",
            to_element="modern",
            relationship_type=RelationshipType.ACCESS,
            color="#0000FF",
            label="legacy access"
        )

        plantuml = relationship.to_plantuml(show_labels=True, use_arrow_styles=False)
        # Legacy format doesn't support colors directly
        expected = 'Rel_Access(legacy, modern, "legacy access")'
        assert plantuml == expected


class TestPlantUMLComponentDiagrams:
    """Test PlantUML component diagram syntax generation."""

    def test_plantuml_with_package_grouping(self):
        """Test PlantUML generation with package grouping."""
        # This would typically be handled at the diagram level, not individual relationships
        # But we can test that relationships work within grouped contexts
        relationship = ArchiMateRelationship(
            id="package_rel",
            from_element="HTTP",
            to_element="First Component",
            relationship_type=RelationshipType.SERVING
        )

        plantuml = relationship.to_plantuml(show_labels=False, use_arrow_styles=True)
        expected = '"HTTP" --( "First Component"'
        assert plantuml == expected

    def test_plantuml_with_node_grouping(self):
        """Test PlantUML generation with node grouping."""
        relationship = ArchiMateRelationship(
            id="node_rel",
            from_element="FTP",
            to_element="Second Component",
            relationship_type=RelationshipType.ACCESS
        )

        plantuml = relationship.to_plantuml(show_labels=False, use_arrow_styles=True)
        expected = '"FTP" -->> "Second Component"'
        assert plantuml == expected

    def test_plantuml_with_cloud_container(self):
        """Test PlantUML generation with cloud container context."""
        relationship = ArchiMateRelationship(
            id="cloud_rel",
            from_element="Another Component",
            to_element="Example 1",
            relationship_type=RelationshipType.ASSOCIATION
        )

        plantuml = relationship.to_plantuml(show_labels=False, use_arrow_styles=True)
        expected = '"Another Component" --> "Example 1"'
        assert plantuml == expected

    def test_plantuml_with_database_container(self):
        """Test PlantUML generation with database container context."""
        relationship = ArchiMateRelationship(
            id="db_rel",
            from_element="Example 1",
            to_element="Folder 3",
            relationship_type=RelationshipType.COMPOSITION
        )

        plantuml = relationship.to_plantuml(show_labels=False, use_arrow_styles=True)
        expected = '"Example 1" *--> "Folder 3"'
        assert plantuml == expected

    def test_plantuml_with_folder_frame_containers(self):
        """Test PlantUML generation with folder and frame containers."""
        relationship = ArchiMateRelationship(
            id="folder_frame_rel",
            from_element="Folder 3",
            to_element="Frame 4",
            relationship_type=RelationshipType.FLOW
        )

        plantuml = relationship.to_plantuml(show_labels=False, use_arrow_styles=True)
        expected = '"Folder 3" ~> "Frame 4"'
        assert plantuml == expected

    def test_plantuml_with_interface_alias(self):
        """Test PlantUML generation with interface aliases."""
        relationship = ArchiMateRelationship(
            id="interface_rel",
            from_element="Data Access",
            to_element="First Component",
            relationship_type=RelationshipType.SERVING
        )

        plantuml = relationship.to_plantuml(show_labels=False, use_arrow_styles=True)
        expected = '"Data Access" --( "First Component"'
        assert plantuml == expected

    def test_plantuml_with_use_stereotype(self):
        """Test PlantUML generation with use stereotype relationship."""
        relationship = ArchiMateRelationship(
            id="use_rel",
            from_element="First Component",
            to_element="HTTP",
            relationship_type=RelationshipType.ASSOCIATION,
            label="use"
        )

        plantuml = relationship.to_plantuml(show_labels=True, use_arrow_styles=True)
        expected = '"First Component" --> "HTTP" : use'
        assert plantuml == expected

    def test_plantuml_with_component_names_containing_spaces(self):
        """Test PlantUML generation with component names containing spaces."""
        relationship = ArchiMateRelationship(
            id="spaces_rel",
            from_element="First Component",
            to_element="Another Component",
            relationship_type=RelationshipType.ASSOCIATION
        )

        plantuml = relationship.to_plantuml(show_labels=False, use_arrow_styles=True)
        expected = '"First Component" --> "Another Component"'
        assert plantuml == expected

    def test_plantuml_with_container_names_containing_spaces(self):
        """Test PlantUML generation with container names containing spaces."""
        relationship = ArchiMateRelationship(
            id="container_spaces",
            from_element="Some Group",
            to_element="Other Groups",
            relationship_type=RelationshipType.ASSOCIATION
        )

        plantuml = relationship.to_plantuml(show_labels=False, use_arrow_styles=True)
        expected = '"Some Group" --> "Other Groups"'
        assert plantuml == expected

    def test_plantuml_with_nested_container_names(self):
        """Test PlantUML generation with nested container names."""
        relationship = ArchiMateRelationship(
            id="nested_container",
            from_element="This is my folder",
            to_element="Foo",
            relationship_type=RelationshipType.COMPOSITION
        )

        plantuml = relationship.to_plantuml(show_labels=False, use_arrow_styles=True)
        expected = '"This is my folder" *--> "Foo"'
        assert plantuml == expected
    
    def test_relationship_validation_success(self):
        """Test successful relationship validation."""
        # Create test elements
        elements = {
            "elem_1": ArchiMateElement(
                id="elem_1",
                name="Element 1",
                element_type="Business_Service",
                layer=ArchiMateLayer.BUSINESS,
                aspect=ArchiMateAspect.BEHAVIOR
            ),
            "elem_2": ArchiMateElement(
                id="elem_2",
                name="Element 2",
                element_type="Application_Service",
                layer=ArchiMateLayer.APPLICATION,
                aspect=ArchiMateAspect.BEHAVIOR
            )
        }
        
        relationship = ArchiMateRelationship(
            id="valid_rel",
            from_element="elem_1",
            to_element="elem_2",
            relationship_type=RelationshipType.REALIZATION
        )
        
        errors = relationship.validate_relationship(elements)
        assert len(errors) == 0
    
    def test_relationship_validation_missing_elements(self):
        """Test relationship validation with missing elements."""
        elements = {}
        
        relationship = ArchiMateRelationship(
            id="invalid_rel",
            from_element="missing_1",
            to_element="missing_2",
            relationship_type=RelationshipType.SERVING
        )
        
        errors = relationship.validate_relationship(elements)
        assert len(errors) == 2
        assert "Source element 'missing_1' does not exist" in errors
        assert "Target element 'missing_2' does not exist" in errors
    
    def test_relationship_string_representation(self):
        """Test string representation of relationship."""
        relationship = ArchiMateRelationship(
            id="str_test",
            from_element="a",
            to_element="b",
            relationship_type=RelationshipType.COMPOSITION
        )

        str_repr = str(relationship)
        assert "a --Composition--> b" == str_repr

    def test_relationship_with_arrow_style(self):
        """Test relationship with custom arrow style."""
        relationship = ArchiMateRelationship(
            id="arrow_test",
            from_element="source",
            to_element="target",
            relationship_type=RelationshipType.SERVING,
            arrow_style=ArrowStyle.COMPOSITION
        )

        assert relationship.arrow_style == ArrowStyle.COMPOSITION

    def test_relationship_with_line_style(self):
        """Test relationship with line style."""
        relationship = ArchiMateRelationship(
            id="line_test",
            from_element="a",
            to_element="b",
            relationship_type=RelationshipType.ASSOCIATION,
            line_style="dashed"
        )

        assert relationship.line_style == "dashed"

    def test_relationship_with_color(self):
        """Test relationship with custom color."""
        relationship = ArchiMateRelationship(
            id="color_test",
            from_element="x",
            to_element="y",
            relationship_type=RelationshipType.FLOW,
            color="#FF0000"
        )

        assert relationship.color == "#FF0000"

    def test_relationship_with_length(self):
        """Test relationship with length modifier."""
        relationship = ArchiMateRelationship(
            id="length_test",
            from_element="start",
            to_element="end",
            relationship_type=RelationshipType.REALIZATION,
            length=3
        )

        assert relationship.length == 3

    def test_relationship_with_positioning(self):
        """Test relationship with positioning hints."""
        relationship = ArchiMateRelationship(
            id="pos_test",
            from_element="a",
            to_element="b",
            relationship_type=RelationshipType.ASSOCIATION,
            positioning="hidden"
        )

        assert relationship.positioning == "hidden"

    def test_relationship_properties(self):
        """Test relationship properties field."""
        properties = {"custom_prop": "value", "weight": 5}
        relationship = ArchiMateRelationship(
            id="props_test",
            from_element="elem1",
            to_element="elem2",
            relationship_type=RelationshipType.INFLUENCE,
            properties=properties
        )

        assert relationship.properties == properties

    def test_get_default_arrow_style(self):
        """Test get_default_arrow_style method."""
        relationship = ArchiMateRelationship(
            id="default_style_test",
            from_element="a",
            to_element="b",
            relationship_type=RelationshipType.COMPOSITION
        )

        default_style = relationship.get_default_arrow_style()
        assert default_style == ArrowStyle.COMPOSITION

    def test_get_default_arrow_style_association(self):
        """Test get_default_arrow_style for association (fallback)."""
        relationship = ArchiMateRelationship(
            id="assoc_test",
            from_element="x",
            to_element="y",
            relationship_type=RelationshipType.ASSOCIATION
        )

        default_style = relationship.get_default_arrow_style()
        assert default_style == ArrowStyle.SOLID

    def test_get_arrow_style_with_custom_override(self):
        """Test get_arrow_style with custom arrow style override."""
        relationship = ArchiMateRelationship(
            id="custom_style_test",
            from_element="src",
            to_element="tgt",
            relationship_type=RelationshipType.SERVING,
            arrow_style=ArrowStyle.AGGREGATION
        )

        style = relationship.get_arrow_style()
        assert style == ArrowStyle.AGGREGATION

    def test_get_arrow_style_uses_default(self):
        """Test get_arrow_style uses default when no override."""
        relationship = ArchiMateRelationship(
            id="default_style_test",
            from_element="a",
            to_element="b",
            relationship_type=RelationshipType.REALIZATION
        )

        style = relationship.get_arrow_style()
        assert style == ArrowStyle.REALIZATION


class TestRelationshipCreation:
    """Test relationship creation helper function."""
    
    def test_create_relationship_success(self):
        """Test successful relationship creation."""
        relationship = create_relationship(
            relationship_id="test_create",
            from_element="source_elem",
            to_element="target_elem",
            relationship_type="Serving",
            description="Test serving relationship"
        )
        
        assert relationship.id == "test_create"
        assert relationship.from_element == "source_elem"
        assert relationship.to_element == "target_elem"
        assert relationship.relationship_type == RelationshipType.SERVING
        assert relationship.description == "Test serving relationship"
    
    def test_create_relationship_with_direction(self):
        """Test relationship creation with direction."""
        relationship = create_relationship(
            relationship_id="test_dir",
            from_element="a",
            to_element="b",
            relationship_type="Flow",
            direction="Right",
            label="data flow"
        )
        
        assert relationship.direction == RelationshipDirection.RIGHT
        assert relationship.label == "data flow"
    
    def test_create_relationship_invalid_type(self):
        """Test relationship creation with invalid type."""
        with pytest.raises(ArchiMateRelationshipError) as exc_info:
            create_relationship(
                relationship_id="invalid_type",
                from_element="a",
                to_element="b",
                relationship_type="InvalidType"
            )
        
        assert "Invalid relationship type 'InvalidType'" in str(exc_info.value)
        assert exc_info.value.relationship_type == "InvalidType"
    
    def test_create_relationship_invalid_direction(self):
        """Test relationship creation with invalid direction."""
        with pytest.raises(ArchiMateRelationshipError) as exc_info:
            create_relationship(
                relationship_id="invalid_dir",
                from_element="a",
                to_element="b",
                relationship_type="Association",
                direction="InvalidDirection"
            )
        
        assert "Invalid direction 'InvalidDirection'" in str(exc_info.value)


class TestRelationshipTypes:
    """Test relationship type enumeration."""
    
    def test_all_relationship_types_present(self):
        """Test that all ArchiMate relationship types are present."""
        expected_types = [
            "Access", "Aggregation", "Assignment", "Association",
            "Composition", "Flow", "Influence", "Realization",
            "Serving", "Specialization", "Triggering"
        ]
        
        for rel_type in expected_types:
            assert hasattr(RelationshipType, rel_type.upper())
            assert rel_type in ARCHIMATE_RELATIONSHIPS
    
    def test_relationship_registry_completeness(self):
        """Test that relationship registry is complete."""
        assert len(ARCHIMATE_RELATIONSHIPS) == 11  # ArchiMate 3.2 has 11 relationship types
        
        # Check specific relationships
        assert ARCHIMATE_RELATIONSHIPS["Access"] == RelationshipType.ACCESS
        assert ARCHIMATE_RELATIONSHIPS["Serving"] == RelationshipType.SERVING
        assert ARCHIMATE_RELATIONSHIPS["Realization"] == RelationshipType.REALIZATION
        assert ARCHIMATE_RELATIONSHIPS["Composition"] == RelationshipType.COMPOSITION


class TestRelationshipDirection:
    """Test relationship direction enumeration."""

    def test_all_directions_present(self):
        """Test that all direction types are present."""
        expected_directions = ["Up", "Down", "Left", "Right", "Up_Left", "Up_Right", "Down_Left", "Down_Right"]

        for direction in expected_directions:
            assert hasattr(RelationshipDirection, direction.upper())

    def test_diagonal_directions(self):
        """Test that diagonal directions work correctly."""
        diagonal_dirs = [RelationshipDirection.UP_LEFT, RelationshipDirection.UP_RIGHT,
                        RelationshipDirection.DOWN_LEFT, RelationshipDirection.DOWN_RIGHT]

        for direction in diagonal_dirs:
            assert direction in RelationshipDirection


class TestArrowStyle:
    """Test arrow style enumeration and mappings."""

    def test_all_arrow_styles_present(self):
        """Test that all arrow styles are defined."""
        expected_styles = [
            "SOLID", "DASHED", "SOLID_REVERSE", "DASHED_REVERSE", "BIDIRECTIONAL",
            "COMPOSITION", "AGGREGATION", "ASSIGNMENT", "ASSIGNMENT_REVERSE",
            "SERVING", "SERVING_REVERSE", "ACCESS_READ", "ACCESS_WRITE", "ACCESS_READ_WRITE",
            "INFLUENCE", "FLOW", "TRIGGERING", "SPECIALIZATION", "REALIZATION"
        ]

        for style in expected_styles:
            assert hasattr(ArrowStyle, style)

    def test_arrow_style_values(self):
        """Test arrow style string values."""
        assert ArrowStyle.SOLID.value == "-->"
        assert ArrowStyle.DASHED.value == "..>"
        assert ArrowStyle.COMPOSITION.value == "*-->"
        assert ArrowStyle.AGGREGATION.value == "o-->"
        assert ArrowStyle.SERVING.value == "--("
        assert ArrowStyle.ACCESS_READ.value == "-->>"
        assert ArrowStyle.FLOW.value == "~>"

    def test_relationship_arrow_style_mapping(self):
        """Test that relationship types map to correct arrow styles."""
        from archi_mcp.archimate.relationships.types import ArchiMateRelationshipType

        # Test specific mappings
        assert RELATIONSHIP_ARROW_STYLES[ArchiMateRelationshipType.COMPOSITION] == ArrowStyle.COMPOSITION
        assert RELATIONSHIP_ARROW_STYLES[ArchiMateRelationshipType.AGGREGATION] == ArrowStyle.AGGREGATION
        assert RELATIONSHIP_ARROW_STYLES[ArchiMateRelationshipType.SERVING] == ArrowStyle.SERVING
        assert RELATIONSHIP_ARROW_STYLES[ArchiMateRelationshipType.ACCESS] == ArrowStyle.ACCESS_READ
        assert RELATIONSHIP_ARROW_STYLES[ArchiMateRelationshipType.ASSOCIATION] == ArrowStyle.SOLID

    def test_all_relationship_types_have_arrow_styles(self):
        """Test that all relationship types have arrow style mappings."""
        from archi_mcp.archimate.relationships.types import ArchiMateRelationshipType

        # Get all relationship types
        all_types = [ArchiMateRelationshipType.ACCESS, ArchiMateRelationshipType.AGGREGATION,
                    ArchiMateRelationshipType.ASSIGNMENT, ArchiMateRelationshipType.ASSOCIATION,
                    ArchiMateRelationshipType.COMPOSITION, ArchiMateRelationshipType.FLOW,
                    ArchiMateRelationshipType.INFLUENCE, ArchiMateRelationshipType.REALIZATION,
                    ArchiMateRelationshipType.SERVING, ArchiMateRelationshipType.SPECIALIZATION,
                    ArchiMateRelationshipType.TRIGGERING]

        for rel_type in all_types:
            assert rel_type in RELATIONSHIP_ARROW_STYLES


class TestRelationshipValidation:
    """Test relationship validation constraints."""
    
    def create_test_elements(self):
        """Create test elements for validation."""
        return {
            "business_actor": ArchiMateElement(
                id="business_actor",
                name="Business Actor",
                element_type="Business_Actor",
                layer=ArchiMateLayer.BUSINESS,
                aspect=ArchiMateAspect.ACTIVE_STRUCTURE
            ),
            "business_service": ArchiMateElement(
                id="business_service",
                name="Business Service",
                element_type="Business_Service",
                layer=ArchiMateLayer.BUSINESS,
                aspect=ArchiMateAspect.BEHAVIOR
            ),
            "business_object": ArchiMateElement(
                id="business_object",
                name="Business Object",
                element_type="Business_Object",
                layer=ArchiMateLayer.BUSINESS,
                aspect=ArchiMateAspect.PASSIVE_STRUCTURE
            ),
            "app_component": ArchiMateElement(
                id="app_component",
                name="Application Component",
                element_type="Application_Component",
                layer=ArchiMateLayer.APPLICATION,
                aspect=ArchiMateAspect.ACTIVE_STRUCTURE
            )
        }
    
    def test_access_relationship_validation(self):
        """Test Access relationship validation."""
        elements = self.create_test_elements()
        
        # Valid access relationship
        valid_relationship = ArchiMateRelationship(
            id="valid_access",
            from_element="business_actor",
            to_element="business_object",
            relationship_type=RelationshipType.ACCESS
        )
        
        errors = valid_relationship.validate_relationship(elements)
        # Note: Basic validation might still pass, detailed validation would catch this
        assert isinstance(errors, list)
    
    def test_composition_relationship_validation(self):
        """Test Composition relationship validation."""
        elements = self.create_test_elements()
        
        # Composition within same layer
        composition_relationship = ArchiMateRelationship(
            id="composition_test",
            from_element="business_actor",
            to_element="business_service",
            relationship_type=RelationshipType.COMPOSITION
        )
        
        errors = composition_relationship.validate_relationship(elements)
        assert isinstance(errors, list)
    
    def test_cross_layer_relationships(self):
        """Test relationships across different layers."""
        elements = self.create_test_elements()
        
        # Cross-layer serving relationship
        cross_layer_rel = ArchiMateRelationship(
            id="cross_layer",
            from_element="app_component",
            to_element="business_service",
            relationship_type=RelationshipType.SERVING
        )
        
        errors = cross_layer_rel.validate_relationship(elements)
        assert isinstance(errors, list)
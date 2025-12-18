"""Tests for advanced PlantUML component diagram features."""

import pytest
import json
from archi_mcp.archimate.generator import ArchiMateGenerator, DiagramLayout, PlantUMLJSONObject
from archi_mcp.archimate.elements.base import (
    ArchiMateElement, ArchiMateLayer, ArchiMateAspect,
    PlantUMLSprite, ComponentGroupingStyle
)
from archi_mcp.archimate.relationships.model import (
    ArchiMateRelationship, RelationshipDirection, ArrowStyle
)
from archi_mcp.archimate.relationships.types import ArchiMateRelationshipType
from archi_mcp.archimate.relationships.model import create_relationship
from archi_mcp.archimate.themes import DiagramTheme


class TestPlantUMLSprites:
    """Test PlantUML sprite functionality."""

    def test_sprite_creation(self):
        """Test creating a PlantUML sprite."""
        sprite = PlantUMLSprite(
            name="$businessProcess",
            width=16,
            height=16,
            scale=16,
            data=[
                "FFFFFFFFFFFFFFFF",
                "FFFFFFFFFFFFFFFF",
                "FFFFFFFFFF0FFFFF",
                "FFFFFFFFFF00FFFF"
            ]
        )

        assert sprite.name == "$businessProcess"
        assert sprite.width == 16
        assert sprite.height == 16
        assert sprite.scale == 16
        assert len(sprite.data) == 4

    def test_sprite_to_plantuml(self):
        """Test sprite PlantUML generation."""
        sprite = PlantUMLSprite(
            name="$testSprite",
            width=8,
            height=8,
            scale=8,
            data=["FF00FF00", "00FF00FF"]
        )

        plantuml = sprite.to_plantuml()
        expected = "sprite $testSprite [8x8/8] {\nFF00FF00\n00FF00FF\n}"
        assert plantuml == expected

    def test_sprite_in_element_stereotype(self):
        """Test using sprites in element stereotypes."""
        generator = ArchiMateGenerator()
        sprite = PlantUMLSprite(
            name="$processIcon",
            width=16,
            height=16,
            scale=16,
            data=["FFFFFFFFFFFFFFFF"] * 16
        )

        element = ArchiMateElement(
            id="process",
            name="Business Process",
            element_type="Business_Process",
            layer=ArchiMateLayer.BUSINESS,
            aspect=ArchiMateAspect.BEHAVIOR,
            stereotype="$processIcon",
            sprites=[sprite]
        )

        generator.add_element(element)
        plantuml = generator.generate_plantuml()

        # Check sprite definition is included
        assert "sprite $processIcon [16x16/16] {" in plantuml
        assert "FFFFFFFFFFFFFFFF" in plantuml

    def test_multiple_sprites_collection(self):
        """Test collecting multiple sprites from elements."""
        generator = ArchiMateGenerator()

        sprite1 = PlantUMLSprite(name="$sprite1", width=16, height=16, scale=16, data=["FF"])
        sprite2 = PlantUMLSprite(name="$sprite2", width=16, height=16, scale=16, data=["00"])

        element1 = ArchiMateElement(
            id="elem1", name="Element 1", element_type="Business_Actor",
            layer=ArchiMateLayer.BUSINESS, aspect=ArchiMateAspect.ACTIVE_STRUCTURE,
            sprites=[sprite1]
        )
        element2 = ArchiMateElement(
            id="elem2", name="Element 2", element_type="Business_Process",
            layer=ArchiMateLayer.BUSINESS, aspect=ArchiMateAspect.BEHAVIOR,
            sprites=[sprite2]
        )

        generator.add_element(element1)
        generator.add_element(element2)

        sprites = generator._collect_sprites()
        sprite_names = {s.name for s in sprites}
        assert sprite_names == {"$sprite1", "$sprite2"}


class TestJSONObjects:
    """Test JSON data display functionality."""

    def test_json_object_creation(self):
        """Test creating PlantUML JSON objects."""
        json_obj = PlantUMLJSONObject(
            name="system_metrics",
            data={
                "performance": {"response_time": "150ms"},
                "version": "1.0.0"
            }
        )

        assert json_obj.name == "system_metrics"
        assert json_obj.data["performance"]["response_time"] == "150ms"

    def test_json_object_to_plantuml(self):
        """Test JSON object PlantUML generation."""
        json_obj = PlantUMLJSONObject(
            name="config",
            data={"key": "value", "number": 42}
        )

        plantuml = json_obj.to_plantuml()
        assert 'json config {\n{\n  "key": "value",\n  "number": 42\n}\n}' == plantuml

    def test_json_object_with_list(self):
        """Test JSON object with list data."""
        json_obj = PlantUMLJSONObject(
            name="servers",
            data=["server1", "server2", "server3"]
        )

        plantuml = json_obj.to_plantuml()
        assert "json servers" in plantuml
        assert '"server1"' in plantuml

    def test_allowmixing_with_json_objects(self):
        """Test that allowmixing is added when JSON objects are present."""
        generator = ArchiMateGenerator()

        # Add a regular element
        element = ArchiMateElement(
            id="comp", name="Component", element_type="Application_Component",
            layer=ArchiMateLayer.APPLICATION, aspect=ArchiMateAspect.ACTIVE_STRUCTURE,
            show_as_component=True
        )
        generator.add_element(element)

        # Add JSON object
        json_obj = PlantUMLJSONObject(name="data", data={"test": "value"})
        generator.add_json_object(json_obj)

        plantuml = generator.generate_plantuml()
        assert "allowmixing" in plantuml
        assert "json data" in plantuml


class TestHideRemoveSystem:
    """Test advanced hide/remove system with tags."""

    def test_element_hiding(self):
        """Test hiding specific elements."""
        generator = ArchiMateGenerator()

        elem1 = ArchiMateElement(
            id="elem1", name="Element 1", element_type="Business_Actor",
            layer=ArchiMateLayer.BUSINESS, aspect=ArchiMateAspect.ACTIVE_STRUCTURE
        )
        elem2 = ArchiMateElement(
            id="elem2", name="Element 2", element_type="Business_Process",
            layer=ArchiMateLayer.BUSINESS, aspect=ArchiMateAspect.BEHAVIOR
        )

        generator.add_element(elem1)
        generator.add_element(elem2)
        generator.hide_elements(["elem1"])

        plantuml = generator.generate_plantuml()
        assert "hide elem1" in plantuml
        assert "Business_Actor(elem1" in plantuml  # Still generated but hidden

    def test_element_removal(self):
        """Test removing specific elements."""
        generator = ArchiMateGenerator()

        elem1 = ArchiMateElement(
            id="elem1", name="Element 1", element_type="Business_Actor",
            layer=ArchiMateLayer.BUSINESS, aspect=ArchiMateAspect.ACTIVE_STRUCTURE
        )
        elem2 = ArchiMateElement(
            id="elem2", name="Element 2", element_type="Business_Process",
            layer=ArchiMateLayer.BUSINESS, aspect=ArchiMateAspect.BEHAVIOR
        )

        generator.add_element(elem1)
        generator.add_element(elem2)
        generator.remove_elements(["elem1"])

        plantuml = generator.generate_plantuml()
        assert "Business_Actor(elem1" not in plantuml  # Completely removed
        assert "Business_Process(elem2" in plantuml

    def test_tag_based_hiding(self):
        """Test hiding elements by tags."""
        generator = ArchiMateGenerator()

        elem1 = ArchiMateElement(
            id="elem1", name="Element 1", element_type="Business_Actor",
            layer=ArchiMateLayer.BUSINESS, aspect=ArchiMateAspect.ACTIVE_STRUCTURE,
            tags=["$important", "$business"]
        )
        elem2 = ArchiMateElement(
            id="elem2", name="Element 2", element_type="Business_Process",
            layer=ArchiMateLayer.BUSINESS, aspect=ArchiMateAspect.BEHAVIOR,
            tags=["$business"]
        )

        generator.add_element(elem1)
        generator.add_element(elem2)
        generator.hide_tags(["$important"])

        plantuml = generator.generate_plantuml()
        assert "hide elem1" in plantuml
        assert "hide elem2" not in plantuml

    def test_tag_based_removal(self):
        """Test removing elements by tags."""
        generator = ArchiMateGenerator()

        elem1 = ArchiMateElement(
            id="elem1", name="Element 1", element_type="Business_Actor",
            layer=ArchiMateLayer.BUSINESS, aspect=ArchiMateAspect.ACTIVE_STRUCTURE,
            tags=["$temporary"]
        )
        elem2 = ArchiMateElement(
            id="elem2", name="Element 2", element_type="Business_Process",
            layer=ArchiMateLayer.BUSINESS, aspect=ArchiMateAspect.BEHAVIOR,
            tags=["$permanent"]
        )

        generator.add_element(elem1)
        generator.add_element(elem2)
        generator.remove_tags(["$temporary"])

        plantuml = generator.generate_plantuml()
        assert "Business_Actor(elem1" not in plantuml
        assert "Business_Process(elem2" in plantuml

    def test_special_naming_rules(self):
        """Test special naming rules for $ prefixed elements."""
        generator = ArchiMateGenerator()

        # Element with $ prefix and no alias should be excluded
        elem1 = ArchiMateElement(
            id="$sprite", name="$sprite", element_type="Business_Actor",
            layer=ArchiMateLayer.BUSINESS, aspect=ArchiMateAspect.ACTIVE_STRUCTURE
        )
        # Element with $ prefix but different alias should be included
        elem2 = ArchiMateElement(
            id="component", name="$sprite", element_type="Business_Process",
            layer=ArchiMateLayer.BUSINESS, aspect=ArchiMateAspect.BEHAVIOR
        )

        generator.add_element(elem1)
        generator.add_element(elem2)

        plantuml = generator.generate_plantuml()
        assert "Business_Actor($sprite" not in plantuml
        assert "Business_Process(component" in plantuml

    def test_restore_elements(self):
        """Test restoring hidden/removed elements."""
        generator = ArchiMateGenerator()

        elem1 = ArchiMateElement(
            id="elem1", name="Element 1", element_type="Business_Actor",
            layer=ArchiMateLayer.BUSINESS, aspect=ArchiMateAspect.ACTIVE_STRUCTURE
        )

        generator.add_element(elem1)
        generator.hide_elements(["elem1"])
        generator.restore_elements(["elem1"])

        plantuml = generator.generate_plantuml()
        assert "hide elem1" not in plantuml

    def test_restore_tags(self):
        """Test restoring elements by tags."""
        generator = ArchiMateGenerator()

        elem1 = ArchiMateElement(
            id="elem1", name="Element 1", element_type="Business_Actor",
            layer=ArchiMateLayer.BUSINESS, aspect=ArchiMateAspect.ACTIVE_STRUCTURE,
            tags=["$hidden"]
        )

        generator.add_element(elem1)
        generator.hide_tags(["$hidden"])
        generator.restore_tags(["$hidden"])

        plantuml = generator.generate_plantuml()
        assert "hide elem1" not in plantuml


class TestLongDescriptions:
    """Test long multi-line descriptions in brackets."""

    def test_long_description_in_component(self):
        """Test long description formatting in components."""
        generator = ArchiMateGenerator()

        element = ArchiMateElement(
            id="server",
            name="Web Server",
            element_type="Node",
            layer=ArchiMateLayer.TECHNOLOGY,
            aspect=ArchiMateAspect.ACTIVE_STRUCTURE,
            show_as_component=True,
            long_description="""Web Server Cluster
Load-balanced infrastructure
- Nginx front-end
- Multiple application nodes
- Auto-scaling enabled"""
        )

        generator.add_element(element)
        plantuml = generator.generate_plantuml()

        assert "component server [" in plantuml
        assert "Web Server Cluster" in plantuml
        assert "Load-balanced infrastructure" in plantuml
        assert "- Nginx front-end" in plantuml

    def test_long_description_vs_regular_description(self):
        """Test that long_description takes precedence over regular description."""
        generator = ArchiMateGenerator()

        element = ArchiMateElement(
            id="comp",
            name="Component",
            element_type="Application_Component",
            layer=ArchiMateLayer.APPLICATION,
            aspect=ArchiMateAspect.ACTIVE_STRUCTURE,
            description="Regular description",
            long_description="Long\ndescription",
            show_as_component=True
        )

        generator.add_element(element)
        plantuml = generator.generate_plantuml()

        assert "component comp [\nLong\ndescription\n]" in plantuml
        assert "Regular description" not in plantuml


class TestArrowDirectionControl:
    """Test enhanced arrow direction control."""

    def test_arrow_length_modifier(self):
        """Test arrow length modifiers."""
        relationship = ArchiMateRelationship(
            id="rel1",
            from_element="elem1",
            to_element="elem2",
            relationship_type=ArchiMateRelationshipType.ASSOCIATION,
            length=3
        )

        plantuml = relationship.to_plantuml(use_arrow_styles=True)
        assert "3" in plantuml  # Length modifier should be included

    def test_positioning_hints(self):
        """Test positioning hints for relationships."""
        relationship = ArchiMateRelationship(
            id="rel1",
            from_element="elem1",
            to_element="elem2",
            relationship_type=ArchiMateRelationshipType.ASSOCIATION,
            positioning="hidden"
        )

        plantuml = relationship.to_plantuml(use_arrow_styles=True)
        assert plantuml.startswith("hidden ")

    def test_complex_directions(self):
        """Test complex directional arrows."""
        relationship = ArchiMateRelationship(
            id="rel1",
            from_element="elem1",
            to_element="elem2",
            relationship_type=ArchiMateRelationshipType.ASSOCIATION,
            direction=RelationshipDirection.UP_LEFT
        )

        plantuml = relationship.to_plantuml(use_arrow_styles=True)
        assert "up-left" in plantuml

    def test_all_directions(self):
        """Test all relationship directions."""
        directions = [
            RelationshipDirection.UP,
            RelationshipDirection.DOWN,
            RelationshipDirection.LEFT,
            RelationshipDirection.RIGHT,
            RelationshipDirection.UP_LEFT,
            RelationshipDirection.UP_RIGHT,
            RelationshipDirection.DOWN_LEFT,
            RelationshipDirection.DOWN_RIGHT
        ]

        for direction in directions:
            relationship = ArchiMateRelationship(
                id=f"rel_{direction.value}",
                from_element="elem1",
                to_element="elem2",
                relationship_type=ArchiMateRelationshipType.ASSOCIATION,
                direction=direction
            )

            plantuml = relationship.to_plantuml(use_arrow_styles=True)
            assert direction.value in plantuml

    def test_arrow_styles_with_directions(self):
        """Test various arrow styles with directions."""
        styles_to_test = [
            ArrowStyle.SOLID,
            ArrowStyle.DASHED,
            ArrowStyle.COMPOSITION,
            ArrowStyle.AGGREGATION,
            ArrowStyle.SERVING
        ]

        for style in styles_to_test:
            relationship = ArchiMateRelationship(
                id=f"rel_{style.name}",
                from_element="elem1",
                to_element="elem2",
                relationship_type=ArchiMateRelationshipType.ASSOCIATION,
                arrow_style=style,
                direction=RelationshipDirection.UP
            )

            plantuml = relationship.to_plantuml(use_arrow_styles=True)
            assert "up" in plantuml


class TestComponentStyling:
    """Test component-specific styling and sprite-based stereotypes."""

    def test_sprite_based_stereotypes(self):
        """Test stereotypes using sprite references."""
        generator = ArchiMateGenerator()

        element = ArchiMateElement(
            id="process",
            name="Business Process",
            element_type="Business_Process",
            layer=ArchiMateLayer.BUSINESS,
            aspect=ArchiMateAspect.BEHAVIOR,
            stereotype="$businessProcess",
            show_as_component=True
        )

        generator.add_element(element)
        plantuml = generator.generate_plantuml()

        assert "<<$businessProcess>>" in plantuml

    def test_component_specific_styling(self):
        """Test component-specific skinparam styling."""
        from archi_mcp.archimate.themes import PlantUMLSkinParams, DiagramStyling, DiagramTheme

        styling = DiagramStyling(theme=DiagramTheme.MODERN)
        skinparams = PlantUMLSkinParams.generate_skinparams(styling)

        # Check for component-specific styling
        component_styling_found = any("skinparam component {" in param for param in skinparams)
        assert component_styling_found

    def test_stereotype_specific_styling(self):
        """Test stereotype-specific component styling."""
        from archi_mcp.archimate.themes import PlantUMLSkinParams, DiagramStyling

        styling = DiagramStyling()
        skinparams = PlantUMLSkinParams.generate_skinparams(styling)

        # Check for layer-specific stereotype styling
        business_styling_found = any("skinparam component<<Business>>" in param for param in skinparams)
        assert business_styling_found

    def test_component_style_variants(self):
        """Test different component style variants."""
        generator = ArchiMateGenerator()

        # Add a test element
        element = ArchiMateElement(
            id="test_comp", name="Test Component", element_type="Application_Component",
            layer=ArchiMateLayer.APPLICATION, aspect=ArchiMateAspect.ACTIVE_STRUCTURE,
            show_as_component=True
        )
        generator.add_element(element)

        # Test uml1 style
        layout = DiagramLayout(component_style="uml1")
        generator.set_layout(layout)
        plantuml = generator.generate_plantuml()
        assert "skinparam componentStyle uml1" in plantuml

        # Test rectangle style
        layout = DiagramLayout(component_style="rectangle")
        generator.set_layout(layout)
        plantuml = generator.generate_plantuml()
        assert "skinparam componentStyle rectangle" in plantuml

        # Test uml2 style (default)
        layout = DiagramLayout(component_style="uml2")
        generator.set_layout(layout)
        plantuml = generator.generate_plantuml()
        assert "skinparam componentStyle uml2" in plantuml


class TestIntegrationScenarios:
    """Test integration of multiple advanced features."""

    def test_complete_advanced_diagram(self):
        """Test a complete diagram with all advanced features."""
        generator = ArchiMateGenerator()

        # Create layout with advanced features
        layout = DiagramLayout(
            theme=DiagramTheme.COLORFUL,
            enable_styling=True,
            use_arrow_styles=True,
            show_legend=True
        )
        generator.set_layout(layout)

        # Create element with sprites
        sprite = PlantUMLSprite(
            name="$businessIcon",
            width=16, height=16, scale=16,
            data=["FFFFFFFFFFFFFFFF"] * 16
        )

        customer = ArchiMateElement(
            id="customer",
            name="Online Customer",
            element_type="Business_Actor",
            layer=ArchiMateLayer.BUSINESS,
            aspect=ArchiMateAspect.ACTIVE_STRUCTURE,
            stereotype="$businessIcon",
            sprites=[sprite],
            tags=["$important"],
            grouping_style=ComponentGroupingStyle.PACKAGE
        )

        # Create server with long description
        server = ArchiMateElement(
            id="web_server",
            name="Web Server",
            element_type="Node",
            layer=ArchiMateLayer.TECHNOLOGY,
            aspect=ArchiMateAspect.ACTIVE_STRUCTURE,
            long_description="Web Server\nHigh availability\nLoad balanced",
            show_as_component=True,
            tags=["$infrastructure", "$critical"]
        )

        # Add elements
        generator.add_element(customer)
        generator.add_element(server)

        # Add relationship with advanced features
        relationship = ArchiMateRelationship(
            id="rel1",
            from_element="customer",
            to_element="web_server",
            relationship_type=ArchiMateRelationshipType.SERVING,
            direction=RelationshipDirection.DOWN,
            length=2,
            label="uses"
        )
        generator.add_relationship(relationship)

        # Add JSON data
        json_data = PlantUMLJSONObject(
            name="metrics",
            data={"performance": "excellent", "uptime": "99.9%"}
        )
        generator.add_json_object(json_data)

        # Test hide/remove functionality
        generator.hide_tags(["$infrastructure"])

        # Generate diagram
        plantuml = generator.generate_plantuml(title="Advanced Features Demo")

        # Verify all features are present
        assert "sprite $businessIcon" in plantuml
        assert "<<$businessIcon>>" in plantuml
        assert "component web_server [" in plantuml
        assert "Web Server" in plantuml
        assert "High availability" in plantuml
        assert "down" in plantuml
        assert "2" in plantuml  # length modifier
        assert "allowmixing" in plantuml
        assert "json metrics" in plantuml
        assert "hide web_server" in plantuml  # hidden due to tag
        assert "title Advanced Features Demo" in plantuml

    def test_generator_clear_with_advanced_features(self):
        """Test clearing generator with all advanced features."""
        generator = ArchiMateGenerator()

        # Add elements, relationships, and JSON objects
        element1 = ArchiMateElement(
            id="test1", name="Test 1", element_type="Business_Actor",
            layer=ArchiMateLayer.BUSINESS, aspect=ArchiMateAspect.ACTIVE_STRUCTURE
        )
        element2 = ArchiMateElement(
            id="test2", name="Test 2", element_type="Business_Process",
            layer=ArchiMateLayer.BUSINESS, aspect=ArchiMateAspect.BEHAVIOR
        )
        generator.add_element(element1)
        generator.add_element(element2)

        relationship = ArchiMateRelationship(
            id="rel", from_element="test1", to_element="test2",
            relationship_type=ArchiMateRelationshipType.ASSOCIATION
        )
        generator.add_relationship(relationship)

        json_obj = PlantUMLJSONObject(name="data", data={"test": "value"})
        generator.add_json_object(json_obj)

        # Set up hide/remove rules
        generator.hide_elements(["test"])
        generator.remove_tags(["$test"])
        generator.hidden_tags.add("$hidden")
        generator.removed_tags.add("$removed")

        # Clear everything
        generator.clear()

        # Verify everything is cleared
        assert len(generator.elements) == 0
        assert len(generator.relationships) == 0
        assert len(generator.json_objects) == 0
        assert len(generator.hidden_elements) == 0
        assert len(generator.removed_elements) == 0
        assert len(generator.hidden_tags) == 0
        assert len(generator.removed_tags) == 0
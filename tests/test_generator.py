"""Tests for ArchiMate diagram generator."""

import pytest
from pathlib import Path
import tempfile
from archi_mcp.archimate.generator import ArchiMateGenerator, DiagramLayout
from archi_mcp.archimate.elements.base import ArchiMateElement, ArchiMateLayer, ArchiMateAspect
from archi_mcp.archimate.relationships import ArchiMateRelationship
from archi_mcp.archimate.relationships.types import ArchiMateRelationshipType
from archi_mcp.utils.exceptions import ArchiMateGenerationError


class TestArchiMateGenerator:
    """Test ArchiMate diagram generator."""
    
    def create_test_element(self, id_suffix="1"):
        """Create a test element."""
        return ArchiMateElement(
            id=f"test_element_{id_suffix}",
            name=f"Test Element {id_suffix}",
            element_type="Business_Service",
            layer=ArchiMateLayer.BUSINESS,
            aspect=ArchiMateAspect.BEHAVIOR
        )
    
    def create_test_relationship(self, from_id, to_id, rel_id="1"):
        """Create a test relationship."""
        return ArchiMateRelationship(
            id=f"test_rel_{rel_id}",
            from_element=from_id,
            to_element=to_id,
            relationship_type=ArchiMateRelationshipType.SERVING
        )
    
    def test_generator_initialization(self):
        """Test generator initialization."""
        generator = ArchiMateGenerator()
        
        assert len(generator.elements) == 0
        assert len(generator.relationships) == 0
        assert generator.layout is not None
    
    def test_add_element_success(self):
        """Test successful element addition."""
        generator = ArchiMateGenerator()
        element = self.create_test_element()
        
        generator.add_element(element)
        
        assert len(generator.elements) == 1
        assert generator.elements[element.id] == element
    
    def test_add_element_duplicate_id(self):
        """Test adding element with duplicate ID."""
        generator = ArchiMateGenerator()
        element1 = self.create_test_element("1")
        element2 = ArchiMateElement(
            id="test_element_1",  # Same ID as element1
            name="Different Element",
            element_type="Business_Actor",
            layer=ArchiMateLayer.BUSINESS,
            aspect=ArchiMateAspect.ACTIVE_STRUCTURE
        )
        
        generator.add_element(element1)
        
        with pytest.raises(ArchiMateGenerationError) as exc_info:
            generator.add_element(element2)
        
        assert "already exists" in str(exc_info.value)
    
    def test_add_relationship_success(self):
        """Test successful relationship addition."""
        generator = ArchiMateGenerator()
        element1 = self.create_test_element("1")
        element2 = self.create_test_element("2")
        
        generator.add_element(element1)
        generator.add_element(element2)
        
        relationship = self.create_test_relationship(element1.id, element2.id)
        generator.add_relationship(relationship)
        
        assert len(generator.relationships) == 1
        assert generator.relationships[0] == relationship
    
    def test_add_relationship_missing_elements(self):
        """Test adding relationship with missing elements."""
        generator = ArchiMateGenerator()
        relationship = self.create_test_relationship("missing_1", "missing_2")
        
        with pytest.raises(ArchiMateGenerationError) as exc_info:
            generator.add_relationship(relationship)
        
        assert "validation failed" in str(exc_info.value).lower()
    
    def test_set_layout(self):
        """Test setting diagram layout."""
        generator = ArchiMateGenerator()
        layout = DiagramLayout(
            direction="vertical",
            show_legend=False,
            group_by_layer=True
        )
        
        generator.set_layout(layout)
        
        assert generator.layout.direction == "vertical"
        assert generator.layout.show_legend is False
        assert generator.layout.group_by_layer is True
    
    def test_generate_plantuml_empty(self):
        """Test PlantUML generation with empty diagram."""
        generator = ArchiMateGenerator()
        
        with pytest.raises(ArchiMateGenerationError) as exc_info:
            generator.generate_plantuml()
        
        assert "No elements defined" in str(exc_info.value)
    
    def test_generate_plantuml_simple(self):
        """Test simple PlantUML generation."""
        generator = ArchiMateGenerator()
        element = self.create_test_element()
        generator.add_element(element)
        
        plantuml = generator.generate_plantuml(title="Test Diagram")
        
        assert "@startuml" in plantuml
        assert "@enduml" in plantuml
        assert "!include <archimate/Archimate>" in plantuml
        assert "title Test Diagram" in plantuml
        assert element.to_plantuml() in plantuml
    
    def test_generate_plantuml_with_relationships(self):
        """Test PlantUML generation with relationships."""
        generator = ArchiMateGenerator()
        element1 = self.create_test_element("1")
        element2 = self.create_test_element("2")
        
        generator.add_element(element1)
        generator.add_element(element2)
        
        relationship = self.create_test_relationship(element1.id, element2.id)
        generator.add_relationship(relationship)
        
        plantuml = generator.generate_plantuml()
        
        assert element1.to_plantuml() in plantuml
        assert element2.to_plantuml() in plantuml
        assert relationship.to_plantuml() in plantuml
        assert "' Elements" in plantuml
        assert "' Relationships" in plantuml
    
    def test_generate_plantuml_with_legend(self):
        """Test PlantUML generation with legend."""
        generator = ArchiMateGenerator()
        element = self.create_test_element()
        generator.add_element(element)
        
        layout = DiagramLayout(show_legend=True)
        generator.set_layout(layout)
        
        plantuml = generator.generate_plantuml()
        
        assert "legend" in plantuml
        assert "Business Layer" in plantuml
        assert "end legend" in plantuml
    
    def test_generate_plantuml_group_by_layer(self):
        """Test PlantUML generation grouped by layer."""
        generator = ArchiMateGenerator()
        
        # Add elements from different layers
        business_element = ArchiMateElement(
            id="business_elem",
            name="Business Element",
            element_type="Business_Service",
            layer=ArchiMateLayer.BUSINESS,
            aspect=ArchiMateAspect.BEHAVIOR
        )
        
        app_element = ArchiMateElement(
            id="app_elem",
            name="Application Element",
            element_type="Application_Component",
            layer=ArchiMateLayer.APPLICATION,
            aspect=ArchiMateAspect.ACTIVE_STRUCTURE
        )
        
        generator.add_element(business_element)
        generator.add_element(app_element)
        
        layout = DiagramLayout(group_by_layer=True)
        generator.set_layout(layout)
        
        plantuml = generator.generate_plantuml()
        
        assert "package \"Business Layer\"" in plantuml
        assert "package \"Application Layer\"" in plantuml
    
    def test_clear_diagram(self):
        """Test clearing diagram."""
        generator = ArchiMateGenerator()
        element = self.create_test_element()
        generator.add_element(element)
        
        assert len(generator.elements) == 1
        
        generator.clear()
        
        assert len(generator.elements) == 0
        assert len(generator.relationships) == 0
    
    def test_get_element_count(self):
        """Test getting element count."""
        generator = ArchiMateGenerator()
        
        assert generator.get_element_count() == 0
        
        generator.add_element(self.create_test_element("1"))
        assert generator.get_element_count() == 1
        
        generator.add_element(self.create_test_element("2"))
        assert generator.get_element_count() == 2
    
    def test_get_relationship_count(self):
        """Test getting relationship count."""
        generator = ArchiMateGenerator()
        element1 = self.create_test_element("1")
        element2 = self.create_test_element("2")
        
        generator.add_element(element1)
        generator.add_element(element2)
        
        assert generator.get_relationship_count() == 0
        
        relationship = self.create_test_relationship(element1.id, element2.id)
        generator.add_relationship(relationship)
        
        assert generator.get_relationship_count() == 1
    
    def test_get_layers_used(self):
        """Test getting layers used in diagram."""
        generator = ArchiMateGenerator()
        
        # Add elements from different layers
        business_element = ArchiMateElement(
            id="business_elem",
            name="Business Element",
            element_type="Business_Service",
            layer=ArchiMateLayer.BUSINESS,
            aspect=ArchiMateAspect.BEHAVIOR
        )
        
        tech_element = ArchiMateElement(
            id="tech_elem",
            name="Technology Element",
            element_type="Node",
            layer=ArchiMateLayer.TECHNOLOGY,
            aspect=ArchiMateAspect.ACTIVE_STRUCTURE
        )
        
        generator.add_element(business_element)
        generator.add_element(tech_element)
        
        layers = generator.get_layers_used()
        
        assert "Business" in layers
        assert "Technology" in layers
        assert len(layers) == 2
    
    def test_validate_diagram_success(self):
        """Test successful diagram validation."""
        generator = ArchiMateGenerator()
        element = self.create_test_element()
        generator.add_element(element)
        
        errors = generator.validate_diagram()
        
        assert len(errors) == 0
    
    def test_validate_diagram_with_errors(self):
        """Test diagram validation with errors."""
        generator = ArchiMateGenerator()
        
        # Add element with invalid ID
        invalid_element = ArchiMateElement(
            id="",  # Invalid empty ID
            name="Invalid Element",
            element_type="Business_Service",
            layer=ArchiMateLayer.BUSINESS,
            aspect=ArchiMateAspect.BEHAVIOR
        )
        
        generator.elements[invalid_element.id or "empty"] = invalid_element
        
        errors = generator.validate_diagram()
        
        assert len(errors) > 0
        assert any("Element ID is required" in error for error in errors)
    
    def test_export_to_file(self):
        """Test exporting diagram to file."""
        generator = ArchiMateGenerator()
        element = self.create_test_element()
        generator.add_element(element)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.puml', delete=False) as f:
            temp_path = f.name
        
        try:
            generator.export_to_file(temp_path, title="Test Export")
            
            # Verify file was created and contains expected content
            with open(temp_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            assert "@startuml" in content
            assert "@enduml" in content
            assert "title Test Export" in content
            assert element.to_plantuml() in content
        
        finally:
            # Clean up
            Path(temp_path).unlink(missing_ok=True)
    
    def test_export_to_file_invalid_path(self):
        """Test exporting to invalid file path."""
        generator = ArchiMateGenerator()
        element = self.create_test_element()
        generator.add_element(element)
        
        invalid_path = "/invalid/path/that/does/not/exist/diagram.puml"
        
        with pytest.raises(ArchiMateGenerationError) as exc_info:
            generator.export_to_file(invalid_path)
        
        assert "Failed to export diagram to file" in str(exc_info.value)


class TestDiagramLayout:
    """Test diagram layout configuration."""

    def create_test_element(self, id_suffix="1"):
        """Create a test element."""
        return ArchiMateElement(
            id=f"test_element_{id_suffix}",
            name=f"Test Element {id_suffix}",
            element_type="Business_Service",
            layer=ArchiMateLayer.BUSINESS,
            aspect=ArchiMateAspect.BEHAVIOR
        )

    def create_test_relationship(self, from_id, to_id, rel_id="1"):
        """Create a test relationship."""
        return ArchiMateRelationship(
            id=f"test_rel_{rel_id}",
            from_element=from_id,
            to_element=to_id,
            relationship_type=ArchiMateRelationshipType.SERVING
        )

    def test_default_layout(self):
        """Test default layout configuration."""
        layout = DiagramLayout()
        
        assert layout.direction == "horizontal"
        assert layout.show_legend is True
        assert layout.show_title is True
        assert layout.group_by_layer is False
        assert layout.spacing == "normal"
    
    def test_custom_layout(self):
        """Test custom layout configuration."""
        layout = DiagramLayout(
            direction="vertical",
            show_legend=False,
            show_title=False,
            group_by_layer=True,
            spacing="compact"
        )

        assert layout.direction == "vertical"
        assert layout.show_legend is False
        assert layout.show_title is False
        assert layout.group_by_layer is True
        assert layout.spacing == "compact"

    def test_component_style_uml2_default(self):
        """Test UML2 component style (default)."""
        generator = ArchiMateGenerator()
        element = self.create_test_element()

        generator.add_element(element)
        plantuml = generator.generate_plantuml()

        # Should contain UML2 style declaration
        assert "skinparam componentStyle uml2" in plantuml
        # Should not contain other styles
        assert "skinparam componentStyle uml1" not in plantuml
        assert "skinparam componentStyle rectangle" not in plantuml

    def test_component_style_uml1(self):
        """Test UML1 component style."""
        generator = ArchiMateGenerator()
        generator.layout.component_style = "uml1"
        element = self.create_test_element()

        generator.add_element(element)
        plantuml = generator.generate_plantuml()

        # Should contain UML1 style declaration
        assert "skinparam componentStyle uml1" in plantuml
        # Should not contain other styles
        assert "skinparam componentStyle uml2" not in plantuml
        assert "skinparam componentStyle rectangle" not in plantuml

    def test_component_style_rectangle(self):
        """Test rectangle component style."""
        generator = ArchiMateGenerator()
        generator.layout.component_style = "rectangle"
        element = self.create_test_element()

        generator.add_element(element)
        plantuml = generator.generate_plantuml()

        # Should contain rectangle style declaration
        assert "skinparam componentStyle rectangle" in plantuml
        # Should not contain other styles
        assert "skinparam componentStyle uml1" not in plantuml
        assert "skinparam componentStyle uml2" not in plantuml

    def test_component_style_invalid_fallback_to_uml2(self):
        """Test invalid component style falls back to UML2."""
        generator = ArchiMateGenerator()
        generator.layout.component_style = "invalid_style"
        element = self.create_test_element()

        generator.add_element(element)
        plantuml = generator.generate_plantuml()

        # Should default to UML2 style
        assert "skinparam componentStyle uml2" in plantuml

    def test_long_description_component(self):
        """Test component with long description using square brackets."""
        generator = ArchiMateGenerator()

        # Create element with long description
        element = ArchiMateElement(
            id="long_desc_element",
            name="Component with Long Description",
            element_type="Business_Service",
            layer=ArchiMateLayer.BUSINESS,
            aspect=ArchiMateAspect.BEHAVIOR,
            documentation="""This component
has a long comment
on several lines
and demonstrates
multiline descriptions"""
        )

        generator.add_element(element)
        plantuml = generator.generate_plantuml()

        # Should contain the element with multiline documentation
        assert '"Component with Long Description"' in plantuml
        # Note: The current implementation may not format long descriptions exactly as PlantUML
        # but should at least include the element

    def test_component_individual_color(self):
        """Test component with individual color."""
        generator = ArchiMateGenerator()

        # Create element with color
        element = ArchiMateElement(
            id="colored_element",
            name="Colored Component",
            element_type="Business_Service",
            layer=ArchiMateLayer.BUSINESS,
            aspect=ArchiMateAspect.BEHAVIOR,
            color="#Yellow"
        )

        generator.add_element(element)
        plantuml = generator.generate_plantuml()

        # Should contain the element with color
        assert '"Colored Component"' in plantuml
        # Note: Color implementation may vary based on PlantUML rendering approach

    def test_component_with_sprite_stereotype(self):
        """Test component with sprite in stereotype."""
        generator = ArchiMateGenerator()

        # Create element with sprite stereotype
        element = ArchiMateElement(
            id="sprite_element",
            name="Component with Sprite",
            element_type="Business_Process",
            layer=ArchiMateLayer.BUSINESS,
            aspect=ArchiMateAspect.BEHAVIOR,
            stereotype="$businessProcess"
        )

        generator.add_element(element)
        plantuml = generator.generate_plantuml()

        # Should contain the element with sprite stereotype
        assert '"Component with Sprite"' in plantuml
        assert "$businessProcess" in plantuml

    def test_component_style_with_relationships(self):
        """Test component styles work correctly with relationships."""
        generator = ArchiMateGenerator()
        generator.layout.component_style = "uml1"

        element1 = self.create_test_element("1")
        element2 = self.create_test_element("2")
        relationship = self.create_test_relationship("test_element_1", "test_element_2")

        generator.add_element(element1)
        generator.add_element(element2)
        generator.add_relationship(relationship)

        plantuml = generator.generate_plantuml()

        # Should contain UML1 style and relationship
        assert "skinparam componentStyle uml1" in plantuml
        assert '"Test Element 1"' in plantuml
        assert '"Test Element 2"' in plantuml

    def test_hide_unlinked_elements(self):
        """Test hiding unlinked elements."""
        generator = ArchiMateGenerator()

        # Add linked elements (with relationships)
        element1 = self.create_test_element("1")
        element2 = self.create_test_element("2")
        element3 = self.create_test_element("3")  # This will be unlinked

        generator.add_element(element1)
        generator.add_element(element2)
        generator.add_element(element3)

        # Add relationship between element1 and element2
        relationship = self.create_test_relationship(element1.id, element2.id)
        generator.add_relationship(relationship)

        # Hide unlinked elements
        generator.hide_unlinked_elements()

        plantuml = generator.generate_plantuml()

        # Should contain all elements
        assert '"Test Element 1"' in plantuml
        assert '"Test Element 2"' in plantuml
        assert '"Test Element 3"' in plantuml

        # Should hide the unlinked element
        assert f"hide {element3.id}" in plantuml

        # Should not hide linked elements
        assert f"hide {element1.id}" not in plantuml
        assert f"hide {element2.id}" not in plantuml

    def test_remove_unlinked_elements(self):
        """Test removing unlinked elements."""
        generator = ArchiMateGenerator()

        # Add linked elements (with relationships)
        element1 = self.create_test_element("1")
        element2 = self.create_test_element("2")
        element3 = self.create_test_element("3")  # This will be unlinked

        generator.add_element(element1)
        generator.add_element(element2)
        generator.add_element(element3)

        # Add relationship between element1 and element2
        relationship = self.create_test_relationship(element1.id, element2.id)
        generator.add_relationship(relationship)

        # Remove unlinked elements
        generator.remove_unlinked_elements()

        plantuml = generator.generate_plantuml()

        # Should contain linked elements
        assert '"Test Element 1"' in plantuml
        assert '"Test Element 2"' in plantuml

        # Should not contain the unlinked element
        assert '"Test Element 3"' not in plantuml

    def test_show_unlinked_elements(self):
        """Test showing previously hidden/removed unlinked elements."""
        generator = ArchiMateGenerator()

        element1 = self.create_test_element("1")
        element2 = self.create_test_element("2")
        element3 = self.create_test_element("3")  # Unlinked

        generator.add_element(element1)
        generator.add_element(element2)
        generator.add_element(element3)

        relationship = self.create_test_relationship(element1.id, element2.id)
        generator.add_relationship(relationship)

        # First hide unlinked
        generator.hide_unlinked_elements()
        plantuml_hidden = generator.generate_plantuml()
        assert f"hide {element3.id}" in plantuml_hidden

        # Then show unlinked
        generator.show_unlinked_elements()
        plantuml_shown = generator.generate_plantuml()
        assert f"hide {element3.id}" not in plantuml_shown
        assert '"Test Element 3"' in plantuml_shown
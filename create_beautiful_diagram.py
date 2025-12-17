#!/usr/bin/env python3
"""
Beautiful ArchiMate Diagram Generator Demo

This script demonstrates the enhanced diagram generation capabilities
with beautiful styling, component features, and advanced layouts.
"""

import json
from pathlib import Path
from src.archi_mcp.archimate.generator import ArchiMateGenerator, DiagramLayout
from src.archi_mcp.archimate.themes import DiagramTheme
from src.archi_mcp.archimate.elements.base import (
    ArchiMateElement, ArchiMateLayer, ArchiMateAspect,
    ComponentGroupingStyle, PortDirection, NotePosition,
    ComponentPort, ElementNote, ComponentInterface
)
from src.archi_mcp.archimate.relationships.model import create_relationship


def create_beautiful_ecommerce_diagram():
    """Create a beautiful e-commerce architecture diagram with enhanced features."""

    # Initialize generator with modern theme
    generator = ArchiMateGenerator()

    # Configure beautiful layout
    layout = DiagramLayout(
        theme=DiagramTheme.COLORFUL,
        direction="horizontal",
        show_legend=True,
        show_title=True,
        group_by_layer=True,
        spacing="normal",
        show_element_types=False,
        show_relationship_labels=True,
        component_style="uml2",
        show_component_icons=True,
        enable_styling=True
    )
    generator.set_layout(layout)

    # Create business layer with grouping and notes
    customer = ArchiMateElement(
        id="customer",
        name="Online Customer",
        element_type="Business_Actor",
        layer=ArchiMateLayer.BUSINESS,
        aspect=ArchiMateAspect.ACTIVE_STRUCTURE,
        description="End customers purchasing products online",
        grouping_style=ComponentGroupingStyle.PACKAGE,
        notes=[
            ElementNote(
                content="Primary revenue source\nHigh conversion focus",
                position=NotePosition.TOP
            )
        ]
    )

    sales_process = ArchiMateElement(
        id="sales_process",
        name="E-Commerce Sales",
        element_type="Business_Process",
        layer=ArchiMateLayer.BUSINESS,
        aspect=ArchiMateAspect.BEHAVIOR,
        description="Complete online sales workflow",
        interfaces=[
            ComponentInterface(
                id="order_intf",
                name="Order Interface",
                description="Order placement interface"
            )
        ]
    )

    # Create application layer with ports and interfaces
    web_app = ArchiMateElement(
        id="web_app",
        name="Web Application",
        element_type="Application_Component",
        layer=ArchiMateLayer.APPLICATION,
        aspect=ArchiMateAspect.ACTIVE_STRUCTURE,
        description="Main e-commerce web application",
        show_as_component=True,
        color="#4CAF50",
        ports=[
            ComponentPort(
                id="http_port",
                name="HTTP/HTTPS",
                direction=PortDirection.BIDIRECTIONAL,
                description="Web interface port"
            ),
            ComponentPort(
                id="api_port",
                name="REST API",
                direction=PortDirection.OUTPUT,
                description="API endpoints"
            )
        ],
        interfaces=[
            ComponentInterface(
                id="user_intf",
                name="User Interface",
                interface_type="()",
                description="User interaction interface"
            )
        ],
        notes=[
            ElementNote(
                content="React-based SPA\nHandles user authentication",
                position=NotePosition.RIGHT
            )
        ]
    )

    payment_gateway = ArchiMateElement(
        id="payment_gateway",
        name="Payment Gateway",
        element_type="Application_Service",
        layer=ArchiMateLayer.APPLICATION,
        aspect=ArchiMateAspect.BEHAVIOR,
        description="Payment processing service",
        show_as_component=True,
        color="#FF9800"
    )

    # Create technology layer with cloud grouping
    web_server = ArchiMateElement(
        id="web_server",
        name="Web Server Cluster",
        element_type="Node",
        layer=ArchiMateLayer.TECHNOLOGY,
        aspect=ArchiMateAspect.ACTIVE_STRUCTURE,
        description="Load-balanced web servers",
        grouping_style=ComponentGroupingStyle.CLOUD,
        color="#2196F3"
    )

    database = ArchiMateElement(
        id="database",
        name="Database Cluster",
        element_type="SystemSoftware",
        layer=ArchiMateLayer.TECHNOLOGY,
        aspect=ArchiMateAspect.PASSIVE_STRUCTURE,
        description="Distributed database system",
        grouping_style=ComponentGroupingStyle.DATABASE,
        color="#9C27B0"
    )

    # Add all elements
    generator.add_element(customer)
    generator.add_element(sales_process)
    generator.add_element(web_app)
    generator.add_element(payment_gateway)
    generator.add_element(web_server)
    generator.add_element(database)

    # Create relationships with enhanced styling
    relationships = [
        create_relationship("r1", "customer", "sales_process", "Triggering",
                          label="initiates purchase"),
        create_relationship("r2", "sales_process", "web_app", "Serving",
                          label="uses application"),
        create_relationship("r3", "web_app", "payment_gateway", "Serving",
                          label="processes payments"),
        create_relationship("r4", "web_app", "web_server", "Assignment",
                          label="hosted on"),
        create_relationship("r5", "web_server", "database", "Access",
                          label="reads/writes data"),
        create_relationship("r6", "payment_gateway", "web_server", "Serving",
                          label="integrates with"),
    ]

    for rel in relationships:
        generator.add_relationship(rel)

    # Generate the beautiful diagram
    plantuml_code = generator.generate_plantuml(
        title="Beautiful E-Commerce Architecture",
        description="Enhanced component diagram showcasing modern styling and advanced features"
    )

    # Save to file
    output_file = "beautiful_ecommerce_diagram.puml"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(plantuml_code)

    print(f"Beautiful e-commerce diagram saved to: {output_file}")
    print("\nFeatures demonstrated:")
    print("✓ Modern colorful theme with custom colors")
    print("✓ Component grouping (package, cloud, database)")
    print("✓ Ports and interfaces on components")
    print("✓ Notes attached to elements")
    print("✓ Enhanced relationship styling")
    print("✓ Layer-based organization")

    return plantuml_code


def create_minimal_business_diagram():
    """Create a minimal business diagram with clean styling."""

    generator = ArchiMateGenerator()

    # Configure minimal layout
    layout = DiagramLayout(
        theme=DiagramTheme.MINIMAL,
        direction="vertical",
        show_legend=False,
        show_title=True,
        group_by_layer=False,
        spacing="wide",
        show_element_types=False,
        show_relationship_labels=True,
        component_style="rectangle",
        enable_styling=True
    )
    generator.set_layout(layout)

    # Simple business elements
    actor = ArchiMateElement(
        id="actor",
        name="Business User",
        element_type="Business_Actor",
        layer=ArchiMateLayer.BUSINESS,
        aspect=ArchiMateAspect.ACTIVE_STRUCTURE
    )

    process = ArchiMateElement(
        id="process",
        name="Core Process",
        element_type="Business_Process",
        layer=ArchiMateLayer.BUSINESS,
        aspect=ArchiMateAspect.BEHAVIOR
    )

    service = ArchiMateElement(
        id="service",
        name="Business Service",
        element_type="Business_Service",
        layer=ArchiMateLayer.BUSINESS,
        aspect=ArchiMateAspect.BEHAVIOR
    )

    generator.add_element(actor)
    generator.add_element(process)
    generator.add_element(service)

    # Simple relationships
    generator.add_relationship(create_relationship("r1", "actor", "process", "Triggering"))
    generator.add_relationship(create_relationship("r2", "process", "service", "Realization"))

    plantuml_code = generator.generate_plantuml(
        title="Minimal Business Diagram",
        description="Clean and simple business process flow"
    )

    output_file = "minimal_business_diagram.puml"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(plantuml_code)

    print(f"Minimal business diagram saved to: {output_file}")
    return plantuml_code


def create_professional_architecture_diagram():
    """Create a professional architecture diagram with all layers."""

    generator = ArchiMateGenerator()

    # Professional theme
    layout = DiagramLayout(
        theme=DiagramTheme.PROFESSIONAL,
        direction="horizontal",
        show_legend=True,
        show_title=True,
        group_by_layer=True,
        spacing="normal",
        show_element_types=True,
        show_relationship_labels=True,
        enable_styling=True
    )
    generator.set_layout(layout)

    # Business layer
    stakeholder = ArchiMateElement(
        id="stakeholder",
        name="Business Stakeholder",
        element_type="Stakeholder",
        layer=ArchiMateLayer.MOTIVATION,
        aspect=ArchiMateAspect.ACTIVE_STRUCTURE
    )

    driver = ArchiMateElement(
        id="driver",
        name="Market Growth",
        element_type="Driver",
        layer=ArchiMateLayer.MOTIVATION,
        aspect=ArchiMateAspect.BEHAVIOR
    )

    capability = ArchiMateElement(
        id="capability",
        name="Digital Capability",
        element_type="Capability",
        layer=ArchiMateLayer.STRATEGY,
        aspect=ArchiMateAspect.BEHAVIOR
    )

    # Application and Technology
    app_component = ArchiMateElement(
        id="app_component",
        name="Enterprise Application",
        element_type="Application_Component",
        layer=ArchiMateLayer.APPLICATION,
        aspect=ArchiMateAspect.ACTIVE_STRUCTURE
    )

    tech_node = ArchiMateElement(
        id="tech_node",
        name="Application Server",
        element_type="Node",
        layer=ArchiMateLayer.TECHNOLOGY,
        aspect=ArchiMateAspect.ACTIVE_STRUCTURE
    )

    # Implementation
    project = ArchiMateElement(
        id="project",
        name="Digital Transformation",
        element_type="Work_Package",
        layer=ArchiMateLayer.IMPLEMENTATION,
        aspect=ArchiMateAspect.BEHAVIOR
    )

    generator.add_element(stakeholder)
    generator.add_element(driver)
    generator.add_element(capability)
    generator.add_element(app_component)
    generator.add_element(tech_node)
    generator.add_element(project)

    # Professional relationships
    relationships = [
        create_relationship("r1", "stakeholder", "driver", "Influence", label="influences"),
        create_relationship("r2", "driver", "capability", "Realization", label="requires"),
        create_relationship("r3", "capability", "app_component", "Realization", label="realized by"),
        create_relationship("r4", "app_component", "tech_node", "Assignment", label="runs on"),
        create_relationship("r5", "project", "app_component", "Realization", label="delivers"),
    ]

    for rel in relationships:
        generator.add_relationship(rel)

    plantuml_code = generator.generate_plantuml(
        title="Professional Enterprise Architecture",
        description="Complete multi-layer architecture with strategic alignment"
    )

    output_file = "professional_architecture_diagram.puml"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(plantuml_code)

    print(f"Professional architecture diagram saved to: {output_file}")
    return plantuml_code


if __name__ == "__main__":
    print("Creating beautiful ArchiMate diagrams...\n")

    # Create multiple beautiful diagrams
    create_beautiful_ecommerce_diagram()
    print()

    create_minimal_business_diagram()
    print()

    create_professional_architecture_diagram()
    print()

    print("All diagrams created successfully!")
    print("\nTo generate PNG images, run:")
    print("java -jar plantuml.jar *.puml")
    print("\nOr use the generator's generate_png_to_tmp() method for programmatic generation.")
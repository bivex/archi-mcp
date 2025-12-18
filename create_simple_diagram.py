#!/usr/bin/env python3
"""Simple script to create a basic ArchiMate diagram."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from archi_mcp.archimate import ArchiMateGenerator, ArchiMateElement
from archi_mcp.archimate.elements.base import ArchiMateLayer

def create_simple_diagram():
    """Create a simple ArchiMate diagram with PlantUML output."""

    # Create generator
    generator = ArchiMateGenerator()

    # Create elements
    customer = ArchiMateElement(
        id="customer",
        name="Customer",
        element_type="Business_Actor",
        layer=ArchiMateLayer.BUSINESS,
        description="End customer"
    )

    service = ArchiMateElement(
        id="service",
        name="Online Service",
        element_type="Business_Service",
        layer=ArchiMateLayer.BUSINESS,
        description="Web service for customers"
    )

    # Add elements to generator
    generator.add_element(customer)
    generator.add_element(service)

    # Add relationship
    generator.add_relationship(
        from_element=customer,
        to_element=service,
        relationship_type="Serving",
        label="uses"
    )

    # Generate PlantUML code
    plantuml_code = generator.generate_plantuml(
        title="Simple Business Diagram",
        description="A simple example diagram"
    )

    print("🎉 Simple ArchiMate Diagram Created!")
    print("=" * 50)
    print()
    print("PlantUML Code:")
    print("-" * 20)
    print(plantuml_code)
    print()
    print("📝 To generate PNG: Save the above code to a .puml file and use PlantUML")
    print("   Example: java -jar plantuml.jar simple_diagram.puml")

if __name__ == "__main__":
    create_simple_diagram()
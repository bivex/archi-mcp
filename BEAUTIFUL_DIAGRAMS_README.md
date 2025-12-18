# Beautiful ArchiMate Diagrams

This document showcases the enhanced diagram generation capabilities that make your ArchiMate diagrams stunning and professional.

## ✨ New Features

### 🎨 Visual Themes
Choose from predefined themes for different styles:

- **Modern**: Clean, professional with subtle shadows and rounded corners
- **Classic**: Traditional styling with solid borders
- **Colorful**: Vibrant colors with enhanced visual appeal
- **Minimal**: Clean and simple, perfect for documentation
- **Dark**: Dark theme for presentations
- **Professional**: Corporate-ready styling

### 🏗️ Component Diagram Features

#### Grouping Styles
Organize elements with different grouping containers:
```python
element.grouping_style = ComponentGroupingStyle.PACKAGE    # Rectangle with header
element.grouping_style = ComponentGroupingStyle.NODE       # Rounded rectangle
element.grouping_style = ComponentGroupingStyle.FOLDER     # Folder icon
element.grouping_style = ComponentGroupingStyle.CLOUD      # Cloud shape
element.grouping_style = ComponentGroupingStyle.DATABASE   # Database cylinder
element.grouping_style = ComponentGroupingStyle.FRAME      # Labeled frame
```

#### Ports and Interfaces
Add detailed component interfaces:
```python
# Add ports to components
web_app.ports = [
    ComponentPort(
        id="http_port",
        name="HTTP/HTTPS",
        direction=PortDirection.BIDIRECTIONAL
    ),
    ComponentPort(
        id="api_port",
        name="REST API",
        direction=PortDirection.OUTPUT
    )
]

# Add interfaces
web_app.interfaces = [
    ComponentInterface(
        id="user_intf",
        name="User Interface",
        interface_type="()"  # Circle notation
    )
]
```

#### Notes and Documentation
Attach contextual information to elements:
```python
element.notes = [
    ElementNote(
        content="This component handles user authentication\nand session management",
        position=NotePosition.RIGHT
    ),
    ElementNote(
        content="Critical performance requirements",
        position=NotePosition.TOP,
        is_floating=True
    )
]
```

### 🔗 Enhanced Relationships

#### Relationship-Specific Arrows
Relationships now use appropriate arrow styles based on their type:

- **Assignment**: `--*` (filled diamond)
- **Aggregation**: `o-->` (empty diamond)
- **Composition**: `*-->` (filled diamond)
- **Serving**: `--(` (circle)
- **Access**: `-->>` (read), `<<--` (write)
- **Specialization**: `--|>` (inheritance)
- **Realization**: `..|>` (dashed inheritance)

#### Directional Hints
Add directional guidance for complex layouts:
```python
relationship.direction = RelationshipDirection.UP
relationship.direction = RelationshipDirection.DOWN
relationship.direction = RelationshipDirection.LEFT
relationship.direction = RelationshipDirection.RIGHT
```

#### Custom Styling
Customize relationship appearance:
```python
relationship.color = "#FF5722"
relationship.line_style = "dashed"  # solid, dashed, dotted
```

### 🎯 Component Rendering Options

#### Render as PlantUML Components
Instead of ArchiMate elements, render as standard PlantUML components:
```python
element.show_as_component = True
element.color = "#4CAF50"  # Custom color
```

#### Custom Colors
Assign specific colors to elements:
```python
element.color = "#FF5722"  # Hex color codes
```

## 🚀 Quick Start

### Basic Beautiful Diagram
```python
from src.archi_mcp.archimate.generator import ArchiMateGenerator, DiagramLayout
from src.archi_mcp.archimate.themes import DiagramTheme

# Create generator with beautiful theme
generator = ArchiMateGenerator()

# Configure layout
layout = DiagramLayout(
    theme=DiagramTheme.COLORFUL,
    direction="horizontal",
    group_by_layer=True,
    enable_styling=True
)
generator.set_layout(layout)

# Add elements and relationships...

# Generate beautiful diagram
plantuml_code = generator.generate_plantuml(
    title="My Beautiful Architecture",
    description="Enhanced with modern styling"
)
```

### Advanced Component Features
```python
from src.archi_mcp.archimate.elements.base import (
    ArchiMateElement, ComponentGroupingStyle,
    ComponentPort, PortDirection, ElementNote, NotePosition
)

# Create component with ports and notes
web_app = ArchiMateElement(
    id="web_app",
    name="Web Application",
    element_type="Application_Component",
    layer=ArchiMateLayer.APPLICATION,
    show_as_component=True,
    color="#4CAF50",
    grouping_style=ComponentGroupingStyle.CLOUD,
    ports=[
        ComponentPort(id="http", name="HTTP", direction=PortDirection.BIDIRECTIONAL),
        ComponentPort(id="api", name="REST API", direction=PortDirection.OUTPUT)
    ],
    notes=[
        ElementNote(
            content="React-based SPA\nHandles 10k concurrent users",
            position=NotePosition.RIGHT
        )
    ]
)

generator.add_element(web_app)
```

## 📊 Examples

### E-Commerce Architecture
See `beautiful_ecommerce_diagram.puml` for a complete example featuring:
- Colorful theme with custom component colors
- Package, cloud, and database grouping
- Component ports and interfaces
- Element notes
- Enhanced relationship styling

### Minimal Business Diagram
See `minimal_business_diagram.puml` for clean, simple styling:
- Minimal theme
- Rectangle component style
- Vertical layout
- Wide spacing

### Professional Architecture
See `professional_architecture_diagram.puml` for enterprise-ready diagrams:
- Professional theme
- Multi-layer organization
- Element type labels
- Comprehensive relationships

## 🎨 Customization

### Creating Custom Themes
```python
from src.archi_mcp.archimate.themes import DiagramStyling, ColorScheme, FontConfig

custom_styling = DiagramStyling(
    theme=DiagramTheme.MODERN,
    colors=ColorScheme(
        background="#F0F8FF",  # Alice blue background
        primary="#4169E1",     # Royal blue
        secondary="#87CEEB",   # Sky blue
        accent="#00CED1"       # Dark turquoise
    ),
    font=FontConfig(
        name="Segoe UI",
        size=11
    ),
    spacing="wide",
    show_shadows=True
)

generator.set_styling(custom_styling)
```

### Layout Options
```python
layout = DiagramLayout(
    direction="vertical",           # horizontal, vertical
    spacing="compact",              # compact, normal, wide
    component_style="rectangle",    # uml1, uml2, rectangle
    show_component_icons=False,     # Hide ArchiMate icons
    enable_styling=True
)
```

## 🔧 Generating Images

### Command Line
```bash
# Generate PNG from PlantUML
java -jar plantuml.jar beautiful_ecommerce_diagram.puml

# Generate multiple diagrams
java -jar plantuml.jar *.puml
```

### Programmatic Generation
```python
# Generate PNG to temporary file
png_path = generator.generate_png_to_tmp(title="My Diagram")
print(f"PNG saved to: {png_path}")
```

## 📈 Benefits

- **Professional Appearance**: Enterprise-ready diagrams
- **Enhanced Readability**: Better visual hierarchy and organization
- **Flexibility**: Multiple themes and customization options
- **Component Details**: Ports, interfaces, and notes for technical accuracy
- **Relationship Clarity**: Meaningful arrow styles and directions
- **Multi-format Support**: PlantUML and PNG generation

## 🎯 Best Practices

1. **Choose Appropriate Themes**: Use colorful themes for presentations, minimal for documentation
2. **Use Grouping Wisely**: Group related components logically
3. **Add Meaningful Notes**: Include performance requirements, constraints, or important details
4. **Leverage Ports**: Show component interfaces clearly
5. **Customize Colors**: Use brand colors or layer-specific colors for better organization
6. **Test Layouts**: Try different directions and spacing for optimal readability

---

*Generated with ❤️ using enhanced ArchiMate diagram generation*</contents>
</xai:function_call">BEAUTIFUL_DIAGRAMS_README.md

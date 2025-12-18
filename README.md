# ArchiMate MCP Server - AI-Powered Enterprise Architecture Modeling

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![FastMCP](https://img.shields.io/badge/FastMCP-2.8+-green.svg)](https://github.com/jlowin/fastmcp)
[![ArchiMate](https://img.shields.io/badge/ArchiMate-3.2-orange.svg)](https://www.opengroup.org/archimate-forum/archimate-overview)
[![PlantUML](https://img.shields.io/badge/PlantUML-Compatible-lightblue.svg)](https://plantuml.com/)
[![MCP Protocol](https://img.shields.io/badge/MCP-Protocol-purple.svg)](https://modelcontextprotocol.io/)
[![Tests](https://img.shields.io/badge/Tests-201%20Passing-brightgreen.svg)](#-development)
[![Coverage](https://img.shields.io/badge/Coverage-59%25-success.svg)](#-development)
[![Production Ready](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)](#-overview)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Compatible-blueviolet.svg)](https://docs.claude.com/en/docs/claude-code)
[![Claude Desktop](https://img.shields.io/badge/Claude%20Desktop-Compatible-blueviolet.svg)](https://claude.ai/download)

AI-powered MCP server for automated ArchiMate diagram generation, enterprise architecture modeling, and business process visualization using PlantUML. Create professional architecture diagrams with Claude AI integration, supporting all 7 ArchiMate layers, 55+ element types, and comprehensive relationship modeling.

> **✨ Claude Code & Claude Desktop Compatible**: Fully tested with both Claude Code CLI and Claude Desktop. Automatic parameter handling ensures seamless operation across both platforms (v1.0.2+).

> **🎯 Live Architecture Demo**: This repository includes a complete architectural blueprint of the ArchiMate MCP Server itself, spanning all 7 ArchiMate layers with 8 coordinated views. See the generated diagrams below for a real-world demonstration of the tool's capabilities.

## 🏗️ Enterprise Architecture Modeling Overview

ArchiMate MCP Server bridges the gap between AI-powered architecture modeling and professional enterprise architecture standards. This specialized Model Context Protocol (MCP) server delivers automated ArchiMate diagram creation, business capability mapping, technology architecture visualization, and comprehensive enterprise modeling using PlantUML. Unlike generic UML tools, it provides complete ArchiMate 3.2 specification compliance with intelligent AI-driven diagram generation, validation, and stakeholder communication features.

### Enterprise Architecture Modeling Key Features

- **Complete ArchiMate 3.2 Compliance**: Full support for 55+ enterprise architecture elements across all 7 ArchiMate layers (Motivation, Strategy, Business, Application, Technology, Physical, Implementation & Migration)
- **Automated PlantUML Diagram Generation**: Professional architecture visualization with official PlantUML ArchiMate sprites and syntax for business process modeling
- **AI-Powered Input Intelligence**: Smart case-insensitive input processing with automatic enterprise architecture element correction and contextual error guidance
- **Enterprise-Grade Validation Pipeline**: 4-step comprehensive validation with real-time architecture modeling error detection and compliance checking
- **Production-Ready Diagram Export**: macOS-optimized PNG/SVG generation with headless rendering, live HTTP server for instant architecture diagram viewing (PlantUML 1.2025.4)
- **MCP Integration Tools**: 2 core Model Context Protocol tools plus 5 expert AI prompts for enterprise architecture modeling, business capability mapping, technology stack visualization, implementation roadmapping, and stakeholder communication
- **Intelligent Error Resolution**: AI-driven troubleshooting with pattern recognition, automated fixes, and architecture modeling best practices guidance
- **Modern MCP Protocol Implementation**: FastMCP 2.8+ integration with comprehensive schema discovery for seamless Claude AI and enterprise architecture workflow integration
- **Production-Quality Testing**: 201 comprehensive test cases with 59% coverage across all ArchiMate layers and enterprise modeling scenarios
- **Multi-Language Architecture Support**: Automatic Slovak/English detection with customizable relationship labels for international enterprise architecture teams
- **Advanced Visualization Controls**: Configurable layout direction, spacing, grouping, and styling options for professional enterprise architecture documentation

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/entira/archi-mcp.git
cd archi-mcp

# Install dependencies with uv
uv sync

# Download PlantUML JAR (required for diagram generation)
curl -L https://github.com/plantuml/plantuml/releases/latest/download/plantuml.jar -o plantuml.jar

# Optional: Test the installation
uv run python -c "import archi_mcp; print('✅ Installation successful!')"
```

### macOS Setup

For optimal performance on macOS, install the required dependencies:

#### Install Java (OpenJDK)
```bash
# Install OpenJDK using Homebrew
brew install openjdk

# Add Java to your PATH (add to ~/.zshrc or ~/.bash_profile)
echo 'export PATH="/opt/homebrew/opt/openjdk/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

#### Install Graphviz (Required for ArchiMate Diagrams)
```bash
# Install Graphviz for diagram generation
brew install graphviz

# Verify installation
dot -v
```

#### Test PlantUML Integration
```bash
# Test that PlantUML can generate diagrams
java -jar plantuml.jar -version

# You should see:
# PlantUML version 1.2025.x
# Dot version: dot - graphviz version x.x.x
# Installation seems OK. File generation OK
```

#### macOS Troubleshooting
- **"Java not found"**: Ensure OpenJDK is in your PATH (see installation steps above)
- **"Dot executable does not exist"**: Install Graphviz using `brew install graphviz`
- **"PlantUML generation fails"**: Ensure both Java and Graphviz are properly installed and accessible
- **Permission issues**: The server needs write access to the `exports/` directory for diagram generation

### Running the MCP Server

#### Direct Execution (for development/testing)
```bash
# Run the MCP server directly
uv run python -m archi_mcp.server

# Or with specific log level
ARCHI_MCP_LOG_LEVEL=DEBUG uv run python -m archi_mcp.server
```

#### Via Claude Desktop
Configure Claude Desktop as shown below, then restart Claude Desktop to load the new MCP server.

#### Via Claude Code CLI
```bash
# Claude Code will automatically discover and use MCP servers
# configured in your claude_desktop_config.json
claude
```

### Upgrading to Latest Version

```bash
# Navigate to your archi-mcp directory
cd archi-mcp

# Fetch latest changes
git fetch origin

# Upgrade to specific version (e.g., v1.0.2)
git checkout v1.0.2

# Or upgrade to latest main branch
git checkout main
git pull origin main

# Update dependencies
uv sync

# Download latest PlantUML JAR if needed
curl -L https://github.com/plantuml/plantuml/releases/latest/download/plantuml.jar -o plantuml.jar
```

### Claude Desktop Configuration (mcp.json)

**📍 Configuration file location:**

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`  
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

**⚠️ Important:** Replace `/path/to/your/archi-mcp` with the actual absolute path to your ArchiMate MCP project directory.

#### Complete configuration:
```json
{
  "mcpServers": {
    "archi-mcp": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/your/archi-mcp", "python", "-m", "archi_mcp.server"],
      "cwd": "/path/to/your/archi-mcp",
      "env": {
        "ARCHI_MCP_LOG_LEVEL": "INFO",
        "ARCHI_MCP_STRICT_VALIDATION": "true",
        "ARCHI_MCP_LANGUAGE": "auto",
        "ARCHI_MCP_DEFAULT_DIRECTION": "top-bottom",
        "ARCHI_MCP_DEFAULT_SPACING": "comfortable",
        "ARCHI_MCP_DEFAULT_TITLE": "true",
        "ARCHI_MCP_DEFAULT_LEGEND": "false",
        "ARCHI_MCP_DEFAULT_GROUP_BY_LAYER": "false",
        "ARCHI_MCP_DEFAULT_SHOW_RELATIONSHIP_LABELS": "true",
        "ARCHI_MCP_LOCK_DIRECTION": "false",
        "ARCHI_MCP_LOCK_SPACING": "false",
        "ARCHI_MCP_LOCK_TITLE": "false",
        "ARCHI_MCP_LOCK_LEGEND": "false",
        "ARCHI_MCP_LOCK_GROUP_BY_LAYER": "false",
        "ARCHI_MCP_LOCK_SHOW_RELATIONSHIP_LABELS": "false"
      }
    }
  }
}
```

**🚀 Setup steps:**
1. Create or edit the `claude_desktop_config.json` file at the location above
2. Add the configuration above, replacing `/path/to/your/archi-mcp` with your actual project path
3. Save the file and restart Claude Desktop
4. The ArchiMate MCP server will be automatically available in Claude Desktop

**✅ Verification:**
After setup, ask Claude: *"What MCP tools are available?"* - you should see `archi-mcp` tools listed.

**🔧 Troubleshooting:**
- **"MCP server not found"**: Check that the path in `"cwd"` and `"args"` is correct and absolute
- **"Command failed"**: Ensure `uv` is installed and `python -m archi_mcp.server` works from your project directory
- **"Import errors"**: Run `uv sync` in your project directory to ensure dependencies are installed
- **"Java not found"**: Ensure Java/OpenJDK is available (see installation steps above)

### Environment Variables

**Core Configuration:**
- **ARCHI_MCP_LOG_LEVEL**: Logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`). Default: `INFO`
- **ARCHI_MCP_STRICT_VALIDATION**: Enable strict ArchiMate validation (`true`/`false`). Default: `true`

**Language Settings:**
- **ARCHI_MCP_LANGUAGE**: Language for relationship labels:
  - `auto`: Auto-detect from content (Slovak/English)
  - `en`: Force English labels
  - `sk`: Force Slovak labels
  - Default: `auto`

**Layout Defaults:**
- **ARCHI_MCP_DEFAULT_DIRECTION**: Default layout direction:
  - `top-bottom`: Vertical top-to-bottom flow
  - `left-right`: Horizontal left-to-right flow  
  - `vertical`: Same as top-bottom
  - `horizontal`: Same as left-right
  - Default: `top-bottom`

- **ARCHI_MCP_DEFAULT_SPACING**: Default element spacing:
  - `compact`: Minimal spacing between elements
  - `balanced`: Moderate spacing for readability
  - `comfortable`: Maximum spacing for clarity
  - Default: `comfortable`

- **ARCHI_MCP_DEFAULT_TITLE**: Show diagram title (`true`/`false`). Default: `true`
- **ARCHI_MCP_DEFAULT_LEGEND**: Show legend with element types (`true`/`false`). Default: `false`
- **ARCHI_MCP_DEFAULT_GROUP_BY_LAYER**: Group elements by ArchiMate layer (`true`/`false`). Default: `false`
- **ARCHI_MCP_DEFAULT_SHOW_RELATIONSHIP_LABELS**: Show enhanced relationship labels (`true`/`false`). Default: `true`

**Parameter Locking (Prevent Client Override):**
- **ARCHI_MCP_LOCK_DIRECTION**: Lock direction parameter (`true`/`false`). Default: `false`
- **ARCHI_MCP_LOCK_SPACING**: Lock spacing parameter (`true`/`false`). Default: `false`
- **ARCHI_MCP_LOCK_TITLE**: Lock title parameter (`true`/`false`). Default: `false`
- **ARCHI_MCP_LOCK_LEGEND**: Lock legend parameter (`true`/`false`). Default: `false`
- **ARCHI_MCP_LOCK_GROUP_BY_LAYER**: Lock grouping parameter (`true`/`false`). Default: `false`
- **ARCHI_MCP_LOCK_SHOW_RELATIONSHIP_LABELS**: Lock relationship labels parameter (`true`/`false`). Default: `false`

**XML Export (Experimental):**
- **ARCHI_MCP_ENABLE_UNIVERSAL_FIX**: Enable universal relationship fixing for Archi compatibility (`true`/`false`). Default: `true`
- **ARCHI_MCP_ENABLE_VALIDATION**: Enable XML validation logging (`true`/`false`). Default: `false`
- **ARCHI_MCP_ENABLE_AUTO_FIX**: Enable automatic relationship correction (`true`/`false`). Default: `false`

**HTTP Server:**
- **ARCHI_MCP_HTTP_PORT**: Port for diagram viewing server (number). Default: `8080`
- **ARCHI_MCP_HTTP_HOST**: Host for diagram server (`localhost`, `0.0.0.0`). Default: `localhost`


### Available MCP Tools

Once configured, ArchiMate MCP Server provides these tools in Claude Desktop:

#### `create_archimate_diagram`
Creates ArchiMate diagrams from natural language descriptions with full parameter control:
- **Input**: Text description, elements, relationships, and optional parameters
- **Output**: Generated diagrams in multiple formats with direct URLs

#### `load_diagram_from_file`
Loads and renders existing ArchiMate diagrams from JSON files:
- **Input**: Path to JSON file with diagram definition
- **Output**: Regenerated diagrams with current PlantUML version

### Basic Usage

**Diagram Generation Example:**
```
Create a simple service-oriented diagram with:
- A customer facing business service
- An application service implementing it
- A supporting technology node
Show how the layers interact.
```

**File Loading Example:**
```
Load the diagram from examples/flower_business_corrected.json and regenerate it.
```

The server automatically:
- Generates all diagram formats (PlantUML, PNG, SVG, XML)
- Starts an HTTP server for instant viewing
- Returns direct URLs for immediate access (e.g., http://localhost:8080/diagram.png)
- Saves all outputs to timestamped directories in `exports/`

## 🏛️ Enterprise Architecture Case Study - Complete ArchiMate Modeling Demo

This repository demonstrates production-ready enterprise architecture modeling through comprehensive architectural documentation of the ArchiMate MCP Server itself. The project showcases all 7 ArchiMate layers with professional-grade PlantUML-generated diagrams, serving as a complete reference implementation for enterprise architecture visualization, business process modeling, and technology stack documentation:

### 🎯 **Complete Layered Architecture Overview**
![ArchiMate MCP Server - Enhanced Layered Architecture](https://raw.githubusercontent.com/entira/archi-mcp/main/docs/diagrams/archi_mcp_layered_architecture_enhanced.svg)
*Comprehensive view showing key elements from all 7 ArchiMate layers with cross-layer relationships*

### 🎯 **Motivation Layer** 
![Motivation View](https://raw.githubusercontent.com/entira/archi-mcp/main/docs/diagrams/archi_mcp_motivation.svg)
*Stakeholders, drivers, goals, and requirements driving the ArchiMate MCP Server implementation*
- **Stakeholders**: Enterprise Architect, Software Developer, Claude Desktop User
- **Drivers**: Architecture Complexity, ArchiMate Compliance, Modeling Automation, AI Integration Demand
- **Goals**: Enable ArchiMate Modeling, Claude Integration, High Quality Diagrams, Comprehensive Validation
- **Requirements**: MCP Protocol Support, ArchiMate 3.2 Support, PlantUML Generation, Real-time Error Analysis

### 📋 **Strategy Layer**
![Strategy View](https://raw.githubusercontent.com/entira/archi-mcp/main/docs/diagrams/archi_mcp_strategy.svg)
*Strategic resources, capabilities, and courses of action for the ArchiMate MCP Server*
- **Resources**: ArchiMate IP Knowledge, Development Team, MCP Ecosystem, Testing Infrastructure
- **Capabilities**: Enterprise Architecture Modeling, Automated Diagram Generation, MCP Protocol Integration, Quality Assurance
- **Courses of Action**: Open Source Strategy, MCP-First Strategy, Standards Compliance Strategy, Continuous Testing Strategy

### 🏢 **Business Layer**
![Business View](https://raw.githubusercontent.com/entira/archi-mcp/main/docs/diagrams/archi_mcp_business.svg)
*Business actors, processes, services, and objects for architecture modeling*
- **Business Actor**: Enterprise Architecture Role (responsible for creating and maintaining enterprise architecture models)
- **Business Processes**: Architecture Modeling Process, Model Validation Process, Error Analysis Process
- **Business Services**: ArchiMate Diagram Service, Architecture Analysis Service, Validation Service
- **Business Objects**: Architecture Model, Diagram Specification, Validation Report

### 💻 **Application Layer**
![Application Structure](https://raw.githubusercontent.com/entira/archi-mcp/main/docs/diagrams/archi_mcp_application.svg)
*Application components, services, and data objects implementing the MCP server*
- **Components**: MCP Server Main, ArchiMate Engine, PlantUML Generator, Validation Engine, HTTP Server
- **Services**: Diagram Generation Service, Architecture Analysis Service, Element Normalization Service, Error Analysis Service
- **Data Objects**: Element Model, Relationship Model, PlantUML Code, Diagram Metadata

### ⚙️ **Technology Layer**
![Technology Layer](https://raw.githubusercontent.com/entira/archi-mcp/main/docs/diagrams/archi_mcp_technology.svg)
*Technology services, system software, nodes, and artifacts supporting the MCP server*
- **Technology Services**: MCP Protocol Service, PlantUML Service, Python Runtime Service, HTTP Service
- **System Software**: Python Interpreter (3.11+), Java Runtime, Operating System
- **Nodes**: Development Environment, Production Environment, Claude Desktop Environment
- **Artifacts**: ArchiMate MCP Server Package, PlantUML JAR (v1.2025.4), Configuration Files

### 🏗️ **Physical Layer**
![Physical Layer](https://raw.githubusercontent.com/entira/archi-mcp/main/docs/diagrams/archi_mcp_physical.svg)
*Physical equipment, facilities, and distribution networks supporting the ArchiMate MCP Server*
- **Equipment**: Developer Workstation, Cloud Server, User Device
- **Facilities**: Development Office, Cloud Datacenter, User Location
- **Distribution Networks**: Development Network, Internet Distribution, Local Network

### 🚀 **Implementation & Migration Layer**
![Implementation & Migration](https://raw.githubusercontent.com/entira/archi-mcp/main/docs/diagrams/archi_mcp_implementation.svg)
*Work packages, deliverables, plateaus, and implementation events for the ArchiMate MCP Server rollout*
- **Work Packages**: Core MCP Implementation, Advanced Features Package, Integration Package, Production Release Package
- **Deliverables**: MCP Protocol Implementation, ArchiMate Engine, Validation Framework, HTTP Server Integration, Test Suite
- **Plateaus**: Development Plateau, Feature Complete Plateau, Integration Plateau, Production Plateau
- **Events**: Project Start, Core Milestone, Feature Milestone, Release Event

> **💡 Complete ArchiMate 3.2 Coverage**: All 7 layers successfully generated using the ArchiMate MCP Server itself, demonstrating 100% layer support and production readiness.

## 🏛️ Comprehensive ArchiMate 3.2 Enterprise Architecture Support

### Complete ArchiMate Layer Modeling

- **Business Layer Architecture**: Business actors, roles, processes, services, and objects for enterprise business process modeling
- **Application Layer Design**: Application components, services, interfaces, and data objects for software architecture visualization
- **Technology Infrastructure Layer**: Technology nodes, devices, system software, networks, and artifacts for IT infrastructure modeling
- **Physical Environment Layer**: Physical equipment, facilities, distribution networks, and materials for infrastructure planning
- **Motivation & Strategy Layer**: Stakeholders, drivers, goals, requirements, principles, resources, capabilities, and value streams for strategic planning
- **Implementation & Migration Layer**: Work packages, deliverables, implementation events, plateaus, and gap analysis for transformation planning

### Enterprise Architecture Relationship Modeling

Complete support for all 12 ArchiMate relationship types with directional variants for comprehensive enterprise modeling:
- Structural Relationships: Access, Aggregation, Assignment, Association, Composition, Specialization
- Dynamic Relationships: Flow, Influence, Triggering
- Dependency Relationships: Serving, Realization

### Advanced Modeling Capabilities

- **Complex Relationship Junctions**: And/Or junctions for sophisticated enterprise architecture relationship modeling
- **Hierarchical Grouping**: Advanced element grouping and nesting for large-scale enterprise architecture diagrams
- **Multi-layer Dependencies**: Cross-layer relationship visualization for enterprise architecture analysis

## 🛠️ AI-Powered MCP Enterprise Architecture Tools

The ArchiMate MCP Server provides 2 core Model Context Protocol tools for automated enterprise architecture modeling and diagram generation via FastMCP integration:

### 1. **create_archimate_diagram** - Automated Architecture Diagram Generation
AI-powered enterprise architecture diagram creation from natural language and structured input:
- Complete support for 55+ ArchiMate element types across all 7 enterprise architecture layers
- Full implementation of 12 ArchiMate relationship types with directional modeling capabilities
- Intelligent AI-driven input normalization and enterprise architecture validation
- Multi-format professional export: PlantUML source, PNG, SVG, and ArchiMate XML for enterprise architecture tools
- Built-in HTTP server with instant viewing URLs for collaborative architecture reviews
- Comprehensive layout and styling configuration for enterprise-grade documentation
- Multi-language enterprise architecture support with automatic Slovak/English detection

### 2. **test_element_normalization** - Architecture Modeling Validation
Enterprise architecture element validation and normalization testing tool:
- Validates intelligent case-insensitive enterprise architecture element processing
- Tests comprehensive ArchiMate element type mappings and business process terminology
- Verifies cross-layer relationship normalization for enterprise architecture compliance
- Essential debugging tool for complex enterprise architecture modeling workflows

### Enterprise Architecture Viewpoints & Modeling Perspectives
- **Layered Architecture View**: Cross-layer enterprise dependencies and relationship mapping for comprehensive business architecture analysis
- **Service Realization View**: How business services are implemented by application components and technology infrastructure
- **Application Cooperation View**: Application component interactions and integration patterns for software architecture design
- **Technology Usage View**: Infrastructure utilization and technology stack dependencies for IT architecture planning
- **Motivation & Strategy View**: Stakeholder analysis, business drivers, strategic goals, and enterprise requirements modeling

### Enterprise Architecture Patterns & Design Templates
- **Three-Tier Enterprise Architecture**: Presentation layer, business logic layer, and data layer separation for scalable enterprise applications
- **Microservices Architecture Pattern**: Service-oriented enterprise architecture with API gateways and distributed system design
- **Event-Driven Architecture**: Asynchronous event processing with producers, consumers, and message flow orchestration for real-time enterprise systems
- **Layered Service Architecture**: Hierarchical service-oriented architecture design for enterprise application integration
- **CQRS Enterprise Pattern**: Command Query Responsibility Segregation for optimized enterprise data management and performance

## 🧪 Enterprise Architecture Tool Development

> 🔧 **For complete enterprise architecture development setup, automated testing, and open source contribution guidelines, see [CLAUDE.md](CLAUDE.md)**

**Quick Start for Developers:**
```bash
git clone https://github.com/entira/archi-mcp.git
cd archi-mcp
uv sync --dev

# Run tests (Java required for PlantUML validation)
export PATH="/opt/homebrew/opt/openjdk/bin:$PATH"
uv run pytest

# Or use the convenience script
./test_with_java.sh
```

### Project Structure

```
archi-mcp/
├── src/archi_mcp/           # Library and server code
│   ├── archimate/           # Modeling components
│   ├── i18n/                # Internationalization
│   ├── xml_export/          # XML export functionality
│   ├── utils/               # Logging and exceptions
│   └── server.py            # FastMCP server entry point
├── tests/                   # Test suites (201 tests, 59% coverage)
├── docs/                    # Documentation and diagrams
```

> **💡 Production Validation**: All architecture diagrams were generated using the ArchiMate MCP Server itself, proving 100% ArchiMate 3.2 layer support and production readiness.

## 🤝 Contributing

> 🔧 **For complete development guidelines, code style, and contribution workflow, see [CLAUDE.md](CLAUDE.md)**

Contributions are welcome! The project follows standard open source practices with comprehensive testing and documentation requirements.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Enterprise Architecture Standards & Technology Acknowledgments

- [ArchiMate® 3.2 Specification](https://www.opengroup.org/archimate-forum/archimate-overview) by The Open Group - Industry standard for enterprise architecture modeling and business process visualization
- [PlantUML](https://plantuml.com/) - Professional diagram generation engine for enterprise architecture documentation and technical visualization
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) - Enabling seamless AI-powered enterprise architecture modeling and automated diagram generation
- [Anthropic](https://www.anthropic.com/) - Claude AI integration for intelligent enterprise architecture analysis and automated modeling workflows

## 🗺️ Enterprise Architecture Modeling Roadmap

- [x] ArchiMate Open Exchange Format XML Export (Experimental enterprise architecture interchange capability)
- **PlantUML Professional Output** - Production-ready enterprise architecture visualization and business process diagrams
- **XML Export Exploration** - Experimental ArchiMate-compliant export for enterprise architecture tool integration
- **Advanced XML Capabilities** - Enhanced validation, auto-correction, and enterprise architecture standards compliance
- [ ] Multi-language Enterprise Support (expanding beyond Slovak/English for global enterprise architecture teams)
- [ ] Custom ArchiMate Viewpoint Templates (pre-built enterprise architecture modeling patterns and frameworks)
- [ ] Enterprise Architecture Repository Integration (connecting with major EA tools and platforms)
- [ ] AI-Powered Architecture Analysis (automated enterprise architecture assessment and optimization recommendations)


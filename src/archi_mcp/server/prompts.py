# Copyright (c) 2025 Bivex
#
# Author: Bivex
# Available for contact via email: support@b-b.top
# For up-to-date contact information:
# https://github.com/bivex
#
# Created: 2025-12-18T11:40:30
# Last Updated: 2025-12-18T11:40:30
#
# Licensed under the MIT License.
# Commercial licensing available upon request.

"""Expert-level MCP Prompts for ArchiMate diagram generation."""

from fastmcp import FastMCP
from typing import Optional

from ..utils.logging import get_logger
from .main import mcp

logger = get_logger(__name__)


@mcp.prompt("enterprise-architecture-analysis")
def enterprise_architecture_analysis(
    business_domain: str,
    current_challenges: str,
    strategic_objectives: str,
    stakeholder_groups: Optional[str] = None,
    technology_landscape: Optional[str] = None
) -> str:
    """Expert prompt for comprehensive enterprise architecture analysis.

    This prompt guides through a systematic enterprise architecture assessment
    using ArchiMate modeling principles to create a holistic view of the organization.

    Args:
        business_domain: Primary business domain or industry sector
        current_challenges: Key challenges and pain points
        strategic_objectives: Strategic goals and objectives
        stakeholder_groups: Key stakeholder groups and their concerns
        technology_landscape: Current technology environment and constraints

    Returns:
        Structured prompt for enterprise architecture analysis
    """
    return f"""# Enterprise Architecture Analysis Expert Prompt

## Context
- **Business Domain**: {business_domain}
- **Current Challenges**: {current_challenges}
- **Strategic Objectives**: {strategic_objectives}
{f"- **Stakeholder Groups**: {stakeholder_groups}" if stakeholder_groups else ""}
{f"- **Technology Landscape**: {technology_landscape}" if technology_landscape else ""}

## Expert Analysis Framework

As an enterprise architecture expert, conduct a comprehensive ArchiMate analysis following this methodology:

### 1. Business Layer Analysis
- Identify core **Business Actors** and their roles
- Map **Business Processes** and **Functions**
- Define **Business Services** and their value propositions
- Establish **Business Objects** and information flows
- Document **Business Events** and triggers

### 2. Application Layer Mapping
- Catalog **Application Components** and their responsibilities
- Define **Application Interfaces** and integration points
- Map **Data Objects** and information assets
- Identify **Application Services** and APIs
- Document **Application Functions** and capabilities

### 3. Technology Layer Assessment
- Inventory **Technology Components** and platforms
- Map **System Software** and middleware
- Define **Technology Interfaces** and protocols
- Identify **Technology Services** and infrastructure capabilities
- Document **Artifacts** and deployment units

### 4. Motivation Layer - Strategic Alignment
- Define **Goals** and **Objectives** from strategic objectives
- Identify **Requirements** and constraints
- Map **Principles** and guidelines
- Document **Stakeholders** and their drivers
- Establish **Value Streams** and outcomes

### 5. Strategy Layer - Capability Planning
- Define **Capabilities** and competencies
- Map **Resources** and assets
- Design **Courses of Action** and initiatives
- Establish **Value Streams** for strategic execution

### 6. Implementation Layer - Execution Planning
- Define **Work Packages** and deliverables
- Establish **Plateaus** and milestones
- Map **Implementation Events** and transitions
- Track **Gaps** and dependencies

### 7. Cross-Layer Relationships
- **Realization** relationships between layers
- **Serving** relationships for service delivery
- **Assignment** relationships for resource allocation
- **Composition/Aggregation** for structural relationships
- **Flow** relationships for information and material flows
- **Influence** relationships for strategic impacts
- **Access** relationships for data and resource usage
- **Triggering** relationships for process flows
- **Specialization** relationships for inheritance hierarchies

### 8. Analysis Deliverables
Generate ArchiMate diagrams that provide:
- **Business Capability Map** - Overview of business capabilities
- **Application Portfolio Map** - Technology landscape view
- **Business Process Flows** - Operational workflows
- **Information Flows** - Data movement and usage
- **Technology Architecture** - Infrastructure and platforms
- **Strategic Roadmap** - Implementation planning
- **Stakeholder Impact Analysis** - Change management view

### 9. Expert Recommendations
Provide specific recommendations for:
- Architecture gaps and improvement opportunities
- Technology modernization priorities
- Process optimization opportunities
- Risk mitigation strategies
- Implementation sequencing and dependencies

Use the `create_archimate_diagram` tool to generate comprehensive ArchiMate diagrams that visualize these architectural insights."""


@mcp.prompt("business-capability-mapping")
def business_capability_mapping(
    organization_type: str,
    core_business_functions: str,
    value_streams: str,
    competitive_differentiators: Optional[str] = None,
    regulatory_requirements: Optional[str] = None
) -> str:
    """Expert prompt for business capability mapping and analysis.

    This prompt focuses on creating a comprehensive business capability map
    that serves as the foundation for enterprise architecture planning.

    Args:
        organization_type: Type of organization (e.g., manufacturing, financial services, healthcare)
        core_business_functions: Primary business functions and operations
        value_streams: Key value streams and customer journeys
        competitive_differentiators: Unique capabilities that provide competitive advantage
        regulatory_requirements: Compliance and regulatory constraints

    Returns:
        Structured prompt for business capability mapping
    """
    return f"""# Business Capability Mapping Expert Prompt

## Organization Context
- **Organization Type**: {organization_type}
- **Core Business Functions**: {core_business_functions}
- **Value Streams**: {value_streams}
{f"- **Competitive Differentiators**: {competitive_differentiators}" if competitive_differentiators else ""}
{f"- **Regulatory Requirements**: {regulatory_requirements}" if regulatory_requirements else ""}

## Expert Capability Mapping Methodology

As a business architecture expert, create a comprehensive capability map following ArchiMate principles:

### 1. Capability Hierarchy Design
- **Level 1**: Strategic Capabilities (core business competencies)
- **Level 2**: Business Capabilities (functional areas)
- **Level 3**: Business Processes (detailed operational capabilities)
- **Level 4**: Activities and Tasks (granular capabilities)

### 2. Strategic Capability Identification
Map strategic capabilities that align with:
- **Customer Experience**: Front-office capabilities
- **Product/Service Delivery**: Core value creation
- **Operational Excellence**: Back-office efficiency
- **Innovation & Growth**: Future-oriented capabilities
- **Risk & Compliance**: Governance and control

### 3. Business Function Decomposition
For each major business function, identify:
- **Business Processes** that execute the capability
- **Business Roles** responsible for execution
- **Business Objects** that are processed
- **Business Services** delivered to customers/stakeholders
- **Business Events** that trigger or result from execution

### 4. Value Stream Mapping
Define end-to-end value streams including:
- **Triggering Events** that initiate value streams
- **Business Functions** that contribute value
- **Business Processes** that execute value creation
- **Business Objects** that carry value
- **Business Services** that deliver value to customers

### 5. Capability Dependencies & Relationships
- **Realization**: How capabilities realize strategic objectives
- **Serving**: How capabilities serve each other
- **Aggregation**: How detailed capabilities form higher-level ones
- **Flow**: Information and material flows between capabilities
- **Influence**: Strategic impacts between capabilities

### 6. Maturity Assessment Framework
For each capability, assess:
- **Current State**: As-is capability maturity
- **Target State**: To-be capability requirements
- **Gaps**: Required improvements and investments
- **Dependencies**: Prerequisites for capability evolution

### 7. Technology Enablement Mapping
Identify technology requirements for each capability:
- **Application Components** that support the capability
- **Technology Services** required for execution
- **Data Objects** and information assets
- **Technology Interfaces** for integration

### 8. Implementation Roadmap
Create phased implementation approach:
- **Work Packages** for capability development
- **Plateaus** representing capability maturity levels
- **Implementation Events** marking transitions
- **Gaps** requiring attention

### 9. Deliverables
Generate ArchiMate diagrams showing:
- **Business Capability Map** - Hierarchical capability structure
- **Value Stream Diagrams** - End-to-end value creation flows
- **Business Process Maps** - Detailed operational workflows
- **Strategic Roadmap** - Capability evolution planning

Use the `create_archimate_diagram` tool to create these visualizations with appropriate styling and layout for maximum clarity and stakeholder communication."""


@mcp.prompt("technology-architecture-design")
def technology_architecture_design(
    target_architecture: str,
    current_technology_stack: str,
    scalability_requirements: str,
    integration_complexity: Optional[str] = None,
    security_requirements: Optional[str] = None,
    compliance_frameworks: Optional[str] = None
) -> str:
    """Expert prompt for technology architecture design and planning.

    This prompt guides through comprehensive technology architecture design
    using ArchiMate to create robust, scalable, and maintainable solutions.

    Args:
        target_architecture: Target architecture pattern (microservices, monolithic, event-driven, etc.)
        current_technology_stack: Existing technology components and platforms
        scalability_requirements: Performance and scaling requirements
        integration_complexity: Integration patterns and complexity level
        security_requirements: Security and compliance requirements
        compliance_frameworks: Specific compliance frameworks (SOX, GDPR, HIPAA, etc.)

    Returns:
        Structured prompt for technology architecture design
    """
    return f"""# Technology Architecture Design Expert Prompt

## Technology Context
- **Target Architecture**: {target_architecture}
- **Current Technology Stack**: {current_technology_stack}
- **Scalability Requirements**: {scalability_requirements}
{f"- **Integration Complexity**: {integration_complexity}" if integration_complexity else ""}
{f"- **Security Requirements**: {security_requirements}" if security_requirements else ""}
{f"- **Compliance Frameworks**: {compliance_frameworks}" if compliance_frameworks else ""}

## Expert Technology Architecture Methodology

As a technology architecture expert, design a comprehensive technology architecture using ArchiMate:

### 1. Technology Layer Foundation
- **Technology Components**: Core technology building blocks
- **System Software**: Operating systems, middleware, runtime environments
- **Technology Interfaces**: APIs, protocols, integration mechanisms
- **Technology Services**: Infrastructure services and capabilities
- **Artifacts**: Deployment units, containers, configuration artifacts

### 2. Architecture Pattern Implementation
Based on target architecture ({target_architecture}), design:
- **Node** structures for deployment topology
- **Device** specifications for hardware requirements
- **Path** definitions for network and communication patterns
- **Technology Collaboration** patterns for distributed systems
- **Technology Function** definitions for computational capabilities

### 3. Scalability & Performance Design
Address scalability requirements through:
- **Horizontal Scaling**: Load distribution patterns
- **Vertical Scaling**: Resource optimization strategies
- **Elasticity**: Dynamic resource allocation
- **Caching Strategies**: Performance optimization approaches
- **Asynchronous Processing**: Non-blocking operation patterns

### 4. Integration Architecture
Design integration patterns for complexity level:
- **Technology Interfaces**: API gateways, message brokers, ESBs
- **Communication Networks**: Event streaming, request-response, pub-sub
- **Protocol Standards**: REST, GraphQL, gRPC, WebSocket
- **Data Synchronization**: Change data capture, event sourcing
- **Service Mesh**: Service discovery, traffic management, observability

### 5. Security Architecture Integration
Implement security requirements through:
- **Security Components**: Authentication, authorization, encryption services
- **Technology Services**: Identity management, access control, audit logging
- **Network Security**: Firewalls, VPNs, zero-trust architectures
- **Data Protection**: Encryption at rest, in transit, and in use
- **Compliance Controls**: Automated compliance monitoring and reporting

### 6. Infrastructure & Deployment Design
Define operational architecture:
- **Technology Nodes**: Servers, containers, serverless functions
- **System Software**: Orchestration platforms, monitoring systems
- **Artifacts**: Docker images, Helm charts, IaC templates
- **Technology Functions**: Backup, recovery, scaling operations

### 7. Application Layer Integration
Map technology support for applications:
- **Application Components** hosted on technology infrastructure
- **Application Interfaces** exposed through technology services
- **Data Objects** persisted in technology storage systems
- **Application Functions** executed on technology platforms

### 8. Migration & Implementation Planning
Create technology transformation roadmap:
- **Current State**: As-is technology architecture assessment
- **Target State**: To-be technology architecture design
- **Transition States**: Intermediate architecture milestones
- **Work Packages**: Technology implementation projects
- **Gaps**: Technology requirements and procurement needs

### 9. Risk Assessment & Mitigation
Identify and address technology risks:
- **Technical Debt**: Legacy system modernization requirements
- **Vendor Lock-in**: Multi-cloud and hybrid cloud strategies
- **Skill Gaps**: Training and hiring requirements
- **Operational Complexity**: Monitoring and management capabilities

### 10. Deliverables
Generate comprehensive ArchiMate diagrams:
- **Technology Architecture Overview** - High-level technology landscape
- **Deployment Diagrams** - Infrastructure and deployment topology
- **Integration Architecture** - System interaction patterns
- **Security Architecture** - Security control implementation
- **Migration Roadmap** - Technology transformation plan

Use the `create_archimate_diagram` tool with appropriate themes (Modern, Professional, Dark) and advanced styling for technical audience consumption."""


@mcp.prompt("implementation-roadmap")
def implementation_roadmap(
    project_scope: str,
    timeline_constraints: str,
    resource_availability: str,
    risk_tolerance: Optional[str] = None,
    change_management_approach: Optional[str] = None,
    success_metrics: Optional[str] = None
) -> str:
    """Expert prompt for creating implementation roadmaps using ArchiMate.

    This prompt guides through systematic implementation planning using
    ArchiMate's Implementation layer concepts and relationships.

    Args:
        project_scope: Scope and boundaries of the implementation project
        timeline_constraints: Time-based constraints and deadlines
        resource_availability: Available resources (budget, people, technology)
        risk_tolerance: Acceptable risk levels and mitigation approaches
        change_management_approach: Stakeholder change management strategy
        success_metrics: Key success indicators and measurement approaches

    Returns:
        Structured prompt for implementation roadmap creation
    """
    return f"""# Implementation Roadmap Expert Prompt

## Implementation Context
- **Project Scope**: {project_scope}
- **Timeline Constraints**: {timeline_constraints}
- **Resource Availability**: {resource_availability}
{f"- **Risk Tolerance**: {risk_tolerance}" if risk_tolerance else ""}
{f"- **Change Management**: {change_management_approach}" if change_management_approach else ""}
{f"- **Success Metrics**: {success_metrics}" if success_metrics else ""}

## Expert Implementation Planning Methodology

As an implementation planning expert, create a comprehensive roadmap using ArchiMate Implementation layer concepts:

### 1. Implementation Layer Foundation
- **Work Packages**: Discrete units of work with clear deliverables
- **Deliverables**: Tangible outputs from work packages
- **Implementation Events**: Milestones and significant occurrences
- **Plateaus**: Stable states representing capability levels
- **Gaps**: Identified deficiencies requiring attention

### 2. Work Breakdown Structure
Decompose implementation into manageable work packages:
- **Planning Phase**: Requirements gathering, analysis, design
- **Development Phase**: Building, testing, integration
- **Deployment Phase**: Release, migration, cutover
- **Operations Phase**: Monitoring, support, optimization
- **Governance**: Program management, risk management, reporting

### 3. Dependency Analysis
Map work package relationships:
- **Triggering**: Sequential dependencies (finish-to-start)
- **Serving**: Support relationships (finish-to-start with ongoing support)
- **Realization**: Work packages that implement requirements/goals
- **Assignment**: Resource allocation to work packages
- **Aggregation**: Work packages that form larger deliverables

### 4. Plateau Design
Define stable intermediate states:
- **Current Plateau**: As-is state baseline
- **Intermediate Plateaus**: Incremental capability improvements
- **Target Plateau**: Final desired state
- **Transition Events**: Changes between plateaus
- **Gap Analysis**: Differences between current and target states

### 5. Timeline & Resource Planning
Align with constraints:
- **Critical Path**: Dependencies that determine minimum timeline
- **Resource Leveling**: Balancing resource utilization
- **Milestone Planning**: Key decision points and checkpoints
- **Risk Buffers**: Contingency time for identified risks
- **Parallel Execution**: Work packages that can run concurrently

### 6. Risk Management Integration
Address risk tolerance through:
- **Risk Assessment**: Probability and impact analysis
- **Mitigation Planning**: Risk response strategies
- **Contingency Work Packages**: Backup implementation approaches
- **Monitoring Events**: Risk trigger points
- **Recovery Plateaus**: Fallback capability states

### 7. Stakeholder Change Management
Implement change management approach:
- **Communication Work Packages**: Stakeholder engagement activities
- **Training Deliverables**: Knowledge transfer materials
- **Change Events**: Adoption milestones and transitions
- **Resistance Mitigation**: Overcoming change barriers
- **Adoption Metrics**: Measuring stakeholder acceptance

### 8. Success Measurement Framework
Define success metrics tracking:
- **Leading Indicators**: Predictive measures of success
- **Lagging Indicators**: Outcome-based success measures
- **Milestone Deliverables**: Checkpoint validation artifacts
- **Quality Gates**: Acceptance criteria for work packages
- **Benefit Realization**: Measuring business value delivery

### 9. Cross-Layer Integration
Connect implementation to enterprise architecture:
- **Business Layer**: Business processes affected by changes
- **Application Layer**: Systems being implemented or modified
- **Technology Layer**: Infrastructure changes required
- **Motivation Layer**: Requirements driving implementation
- **Strategy Layer**: Capabilities being delivered

### 10. Implementation Roadmap Deliverables
Generate comprehensive ArchiMate diagrams:
- **Implementation Roadmap**: Timeline view of work packages and milestones
- **Work Package Dependencies**: Critical path and relationship analysis
- **Plateau Transition Diagram**: Capability evolution visualization
- **Risk Mitigation Plan**: Risk response strategy mapping
- **Resource Allocation Map**: Resource assignment and utilization
- **Success Tracking Dashboard**: Metrics and KPI visualization

Use the `create_archimate_diagram` tool with timeline-appropriate layouts, clear milestone markers, and stakeholder-appropriate styling (Professional theme recommended). Include detailed work package descriptions, success criteria, and dependency relationships for maximum implementation clarity."""


@mcp.prompt("stakeholder-analysis-mapping")
def stakeholder_analysis_mapping(
    stakeholder_ecosystem: str,
    influence_power_matrix: str,
    communication_channels: str,
    change_impact_assessment: Optional[str] = None,
    engagement_strategy: Optional[str] = None,
    resistance_factors: Optional[str] = None
) -> str:
    """Expert prompt for stakeholder analysis and mapping using ArchiMate.

    This prompt creates comprehensive stakeholder maps that identify,
    analyze, and plan engagement strategies for enterprise initiatives.

    Args:
        stakeholder_ecosystem: Key stakeholder groups and individuals
        influence_power_matrix: Power and influence assessment
        communication_channels: Available communication methods
        change_impact_assessment: How stakeholders are affected by changes
        engagement_strategy: Planned stakeholder engagement approach
        resistance_factors: Potential barriers and resistance points

    Returns:
        Structured prompt for stakeholder analysis mapping
    """
    return f"""# Stakeholder Analysis & Mapping Expert Prompt

## Stakeholder Context
- **Stakeholder Ecosystem**: {stakeholder_ecosystem}
- **Influence/Power Matrix**: {influence_power_matrix}
- **Communication Channels**: {communication_channels}
{f"- **Change Impact**: {change_impact_assessment}" if change_impact_assessment else ""}
{f"- **Engagement Strategy**: {engagement_strategy}" if engagement_strategy else ""}
{f"- **Resistance Factors**: {resistance_factors}" if resistance_factors else ""}

## Expert Stakeholder Analysis Methodology

As a stakeholder management expert, create comprehensive stakeholder maps using ArchiMate Motivation layer concepts:

### 1. Stakeholder Identification & Profiling
Map all relevant stakeholders:
- **Stakeholders**: Individuals and groups with interests in the initiative
- **Drivers**: External and internal factors influencing stakeholders
- **Assessments**: Stakeholder evaluations and judgments
- **Goals**: Desired outcomes from stakeholder perspectives
- **Outcomes**: Actual results experienced by stakeholders

### 2. Power & Influence Analysis
Create stakeholder power-interest matrix:
- **High Power/High Interest**: Key players requiring active management
- **High Power/Low Interest**: Keep satisfied with minimal effort
- **Low Power/High Interest**: Keep informed and involved
- **Low Power/Low Interest**: Monitor with minimal effort

### 3. Interest & Concern Mapping
Document stakeholder perspectives:
- **Business Drivers**: Commercial and operational motivations
- **Personal Drivers**: Individual career and professional interests
- **Risk Concerns**: Perceived threats and uncertainties
- **Benefit Expectations**: Anticipated value and advantages
- **Change Impacts**: Personal and professional effects

### 4. Communication Architecture
Design stakeholder communication:
- **Business Interfaces**: Formal communication channels
- **Business Services**: Stakeholder engagement services
- **Business Objects**: Communication artifacts and materials
- **Business Events**: Communication triggers and milestones
- **Business Functions**: Communication planning and execution

### 5. Relationship Mapping
Define stakeholder interdependencies:
- **Association**: General stakeholder relationships
- **Influence**: How stakeholders affect each other
- **Serving**: Support relationships between stakeholders
- **Aggregation**: Stakeholder groups and hierarchies
- **Flow**: Information flow between stakeholder groups

### 6. Change Impact Assessment
Analyze transformation effects:
- **Affected Business Processes**: Operational changes experienced
- **Modified Business Roles**: Job changes and new responsibilities
- **Changed Business Services**: Service delivery modifications
- **Updated Business Objects**: Information and artifact changes
- **Triggered Business Events**: New occurrences and milestones

### 7. Resistance Analysis
Identify and address resistance factors:
- **Assessment Elements**: Stakeholder evaluations of change
- **Driver Analysis**: Root causes of resistance
- **Value Impact**: Perceived losses and gains
- **Principle Conflicts**: Contradictions with stakeholder values
- **Constraint Identification**: Limitations preventing acceptance

### 8. Engagement Strategy Design
Create stakeholder engagement plans:
- **Communication Work Packages**: Engagement activities and campaigns
- **Training Deliverables**: Knowledge transfer and skill development
- **Participation Events**: Stakeholder involvement milestones
- **Feedback Mechanisms**: Two-way communication channels
- **Success Metrics**: Engagement effectiveness measures

### 9. Risk Mitigation Planning
Address stakeholder-related risks:
- **Contingency Plans**: Backup engagement strategies
- **Escalation Paths**: Issue resolution procedures
- **Monitoring Work Packages**: Stakeholder sentiment tracking
- **Intervention Events**: Critical engagement moments
- **Recovery Strategies**: Addressing engagement failures

### 10. Implementation Integration
Connect to implementation planning:
- **Work Package Assignment**: Stakeholder responsibilities
- **Plateau Communication**: Capability level announcements
- **Implementation Event Communication**: Milestone notifications
- **Gap Communication**: Addressing stakeholder concerns
- **Benefit Communication**: Value realization messaging

### 11. Stakeholder Analysis Deliverables
Generate comprehensive ArchiMate diagrams:
- **Stakeholder Map**: Power-interest matrix visualization
- **Stakeholder Relationship Diagram**: Interdependency mapping
- **Communication Architecture**: Engagement channel design
- **Change Impact Assessment**: Affected stakeholder visualization
- **Engagement Roadmap**: Communication and involvement planning
- **Risk Mitigation Plan**: Stakeholder risk response strategies

Use the `create_archimate_diagram` tool with clear stakeholder categorization, relationship visualization, and professional styling appropriate for executive and management audiences. Include stakeholder personas, influence levels, and engagement requirements for maximum strategic value."""
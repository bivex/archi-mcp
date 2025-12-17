"""Base ArchiMate element definition."""

from enum import Enum
from typing import Any, Dict, List, Optional, Set, Union
from pydantic import BaseModel, Field, Field


class ArchiMateLayer(str, Enum):
    """ArchiMate layers according to ArchiMate 3.2 specification."""
    BUSINESS = "Business"
    APPLICATION = "Application"
    TECHNOLOGY = "Technology"
    PHYSICAL = "Physical"
    MOTIVATION = "Motivation"
    STRATEGY = "Strategy"
    IMPLEMENTATION = "Implementation"

    @classmethod
    def get_core_layers(cls) -> Set['ArchiMateLayer']:
        """Get the three core operational layers."""
        return {cls.BUSINESS, cls.APPLICATION, cls.TECHNOLOGY}

    @classmethod
    def get_governance_layers(cls) -> Set['ArchiMateLayer']:
        """Get the governance layers."""
        return {cls.MOTIVATION, cls.STRATEGY}

    @classmethod
    def get_realization_layers(cls) -> Set['ArchiMateLayer']:
        """Get the realization layers."""
        return {cls.IMPLEMENTATION, cls.PHYSICAL}

    def get_layer_description(self) -> str:
        """Get a human-readable description of this layer."""
        descriptions = {
            ArchiMateLayer.BUSINESS: "Business operations and processes",
            ArchiMateLayer.APPLICATION: "Application services and components",
            ArchiMateLayer.TECHNOLOGY: "Technology infrastructure and platforms",
            ArchiMateLayer.PHYSICAL: "Physical infrastructure and facilities",
            ArchiMateLayer.MOTIVATION: "Motivational drivers and requirements",
            ArchiMateLayer.STRATEGY: "Strategic capabilities and resources",
            ArchiMateLayer.IMPLEMENTATION: "Implementation projects and deliverables"
        }
        return descriptions.get(self, "Layer")

    def get_layer_color(self) -> str:
        """Get the default PlantUML color for this layer."""
        colors = {
            ArchiMateLayer.BUSINESS: "Business",
            ArchiMateLayer.APPLICATION: "Application",
            ArchiMateLayer.TECHNOLOGY: "Technology",
            ArchiMateLayer.PHYSICAL: "Physical",
            ArchiMateLayer.MOTIVATION: "Motivation",
            ArchiMateLayer.STRATEGY: "Strategy",
            ArchiMateLayer.IMPLEMENTATION: "Implementation",
        }
        return colors.get(self, "Technology")

    def is_core_layer(self) -> bool:
        """Check if this is a core operational layer."""
        return self in self.get_core_layers()

    def is_governance_layer(self) -> bool:
        """Check if this is a governance layer."""
        return self in self.get_governance_layers()

    def is_realization_layer(self) -> bool:
        """Check if this is a realization layer."""
        return self in self.get_realization_layers()


class ComponentGroupingStyle(str, Enum):
    """Component grouping styles for PlantUML."""
    PACKAGE = "package"
    NODE = "node"
    FOLDER = "folder"
    FRAME = "frame"
    CLOUD = "cloud"
    DATABASE = "database"
    RECTANGLE = "rectangle"


class PortDirection(str, Enum):
    """Port direction for component interfaces."""
    INPUT = "portin"
    OUTPUT = "portout"
    BIDIRECTIONAL = "port"


class NotePosition(str, Enum):
    """Note position relative to elements."""
    TOP = "top"
    BOTTOM = "bottom"
    LEFT = "left"
    RIGHT = "right"


class ElementNote(BaseModel):
    """Note attached to an element."""
    content: str = Field(..., description="Note content")
    position: NotePosition = Field(NotePosition.RIGHT, description="Note position")
    is_floating: bool = Field(False, description="Whether note is floating (not attached to element)")
    background_color: Optional[str] = Field(None, description="Note background color")
    border_color: Optional[str] = Field(None, description="Note border color")


class ComponentPort(BaseModel):
    """Port definition for component interfaces."""
    id: str = Field(..., description="Unique port identifier")
    name: str = Field(..., description="Port name")
    direction: PortDirection = Field(PortDirection.BIDIRECTIONAL, description="Port direction")
    interface_type: Optional[str] = Field(None, description="Interface type or protocol")
    description: Optional[str] = Field(None, description="Port description")




class ComponentInterface(BaseModel):
    """Interface definition for components."""
    id: str = Field(..., description="Unique interface identifier")
    name: str = Field(..., description="Interface display name")
    interface_type: str = Field("()", description="PlantUML interface symbol")
    description: Optional[str] = Field(None, description="Interface description")
    ports: List[ComponentPort] = Field(default_factory=list, description="Associated ports")


class ArchiMateAspect(str, Enum):
    """ArchiMate aspects according to ArchiMate 3.2 specification."""
    ACTIVE_STRUCTURE = "Active Structure"
    PASSIVE_STRUCTURE = "Passive Structure"
    BEHAVIOR = "Behavior"

    def get_aspect_description(self) -> str:
        """Get a human-readable description of this aspect."""
        descriptions = {
            self.ACTIVE_STRUCTURE: "Elements that exhibit behavior and have agency",
            self.PASSIVE_STRUCTURE: "Elements that represent knowledge or data",
            self.BEHAVIOR: "Elements that represent behavior and processes"
        }
        return descriptions.get(self, "Aspect")

    def is_structure_aspect(self) -> bool:
        """Check if this is a structural aspect."""
        return self in {self.ACTIVE_STRUCTURE, self.PASSIVE_STRUCTURE}


class ArchiMateElement(BaseModel):
    """Base class for all ArchiMate elements."""

    id: str = Field(..., description="Unique identifier for the element")
    name: str = Field(..., description="Display name of the element")
    element_type: str = Field(..., description="ArchiMate element type")
    layer: ArchiMateLayer = Field(..., description="ArchiMate layer")
    aspect: ArchiMateAspect = Field(..., description="ArchiMate aspect")
    description: Optional[str] = Field(None, description="Element description")
    stereotype: Optional[str] = Field(None, description="Element stereotype")
    properties: Dict[str, Any] = Field(default_factory=dict, description="Additional properties")
    documentation: Optional[str] = Field(None, description="Element documentation")

    # Component diagram features
    grouping_style: Optional[ComponentGroupingStyle] = Field(None, description="Grouping style for this element")
    notes: List[ElementNote] = Field(default_factory=list, description="Notes attached to this element")
    interfaces: List[ComponentInterface] = Field(default_factory=list, description="Component interfaces")
    ports: List[ComponentPort] = Field(default_factory=list, description="Component ports")
    color: Optional[str] = Field(None, description="Custom color for this element")
    show_as_component: bool = Field(False, description="Render as PlantUML component instead of ArchiMate element")
    
    def to_plantuml(self, show_element_type: bool = False, show_documentation: bool = False) -> str:
        """Generate PlantUML code for this element.

        Args:
            show_element_type: Whether to display element type name in diagram

        Returns:
            PlantUML code string
        """
        lines = []

        # Handle grouping styles
        if self.grouping_style:
            lines.extend(self._generate_grouping_start())

        # Generate main element
        if self.show_as_component:
            lines.append(self._generate_as_component(show_element_type))
        else:
            lines.append(self._generate_as_archimate_element(show_element_type))

        # Add interfaces
        for interface in self.interfaces:
            lines.append(self._generate_interface(interface))

        # Add ports
        for port in self.ports:
            lines.append(self._generate_port(port))

        # Add notes
        for note in self.notes:
            lines.append(self._generate_note(note))

        # Add documentation as note if requested and present
        if show_documentation and self.documentation and not self.notes:
            doc_note = ElementNote(
                content=self.documentation,
                position=NotePosition.BOTTOM,
                is_floating=False
            )
            lines.append(self._generate_note(doc_note))

        # Close grouping if started
        if self.grouping_style:
            lines.append(self._generate_grouping_end())

        return "\n".join(lines)

    def _generate_as_component(self, show_element_type: bool = False) -> str:
        """Generate this element as a PlantUML component."""
        safe_name = self.name.encode('utf-8').decode('utf-8')

        # Build component declaration
        component_parts = []

        if self.color:
            component_parts.append(f"[{safe_name}] #{self.color}")
        else:
            component_parts.append(f"[{safe_name}]")

        if self.stereotype:
            component_parts.append(f" <<{self.stereotype}>>")

        # Add alias
        component_parts.append(f" as {self.id}")

        return "".join(component_parts)

    def _generate_as_archimate_element(self, show_element_type: bool = False) -> str:
        """Generate this element as an ArchiMate element."""
        # Get color based on layer
        color = self._get_layer_color()

        # Build stereotype if present
        stereotype_str = ""
        if self.stereotype:
            stereotype_str = f" <<{self.stereotype}>>"

        # Use local normalization for PlantUML element types
        plantuml_element_type = self._normalize_for_plantuml(self.element_type, self.layer.value)

        # Generate PlantUML archimate element
        # Ensure proper UTF-8 encoding for names with diacritics
        safe_name = self.name.encode('utf-8').decode('utf-8')

        # Add element type to name if requested
        if show_element_type:
            display_name = f"{safe_name}\\n<<{self.element_type}>>"
        else:
            display_name = safe_name

        plantuml_code = f'{plantuml_element_type}({self.id}, "{display_name}"{stereotype_str})'

        return plantuml_code

    def _generate_grouping_start(self) -> List[str]:
        """Generate grouping start syntax."""
        if not self.grouping_style:
            return []

        safe_name = self.name.encode('utf-8').decode('utf-8')

        if self.grouping_style == ComponentGroupingStyle.PACKAGE:
            return [f"package \"{safe_name}\" {{"]
        elif self.grouping_style == ComponentGroupingStyle.NODE:
            return [f"node \"{safe_name}\" {{"]
        elif self.grouping_style == ComponentGroupingStyle.FOLDER:
            return [f"folder \"{safe_name}\" {{"]
        elif self.grouping_style == ComponentGroupingStyle.FRAME:
            return [f"frame \"{safe_name}\" {{"]
        elif self.grouping_style == ComponentGroupingStyle.CLOUD:
            return [f"cloud \"{safe_name}\" {{"]
        elif self.grouping_style == ComponentGroupingStyle.DATABASE:
            return [f"database \"{safe_name}\" {{"]
        elif self.grouping_style == ComponentGroupingStyle.RECTANGLE:
            return [f"rectangle \"{safe_name}\" {{"]
        else:
            return []

    def _generate_grouping_end(self) -> str:
        """Generate grouping end syntax."""
        return "}"

    def _generate_interface(self, interface: ComponentInterface) -> str:
        """Generate PlantUML interface code."""
        safe_name = interface.name.encode('utf-8').decode('utf-8')
        return f'{interface.interface_type} "{safe_name}" as {interface.id}'

    def _generate_port(self, port: ComponentPort) -> str:
        """Generate PlantUML port code."""
        safe_name = port.name.encode('utf-8').decode('utf-8')

        # Add interface type if specified
        interface_part = ""
        if port.interface_type:
            interface_part = f" ({port.interface_type})"

        # Add description if specified
        desc_part = ""
        if port.description:
            desc_part = f"\\n{port.description}"

        return f'{port.direction.value} {port.id} [[{safe_name}{interface_part}{desc_part}]]'

    def _generate_note(self, note: ElementNote) -> str:
        """Generate PlantUML note code."""
        content_lines = note.content.split('\n')

        # Add color styling if specified
        color_style = ""
        if note.background_color or note.border_color:
            color_parts = []
            if note.background_color:
                color_parts.append(f"#{note.background_color}")
            if note.border_color:
                color_parts.append(f"line:{note.border_color}")
            if color_parts:
                color_style = f" {','.join(color_parts)}"

        if len(content_lines) == 1:
            # Single line note
            if note.is_floating:
                return f"note{color_style} as {self.id}_note\n{note.content}\nend note"
            else:
                return f"note{color_style} {note.position.value} of {self.id}: {note.content}"
        else:
            # Multi-line note
            if note.is_floating:
                lines = [f"note{color_style} as {self.id}_note"]
                lines.extend(content_lines)
                lines.append("end note")
                return "\n".join(lines)
            else:
                lines = [f"note{color_style} {note.position.value} of {self.id}"]
                lines.extend(content_lines)
                lines.append("end note")
                return "\n".join(lines)
    
    def _get_layer_color(self) -> str:
        """Get the default color for this layer.

        Returns:
            Color string for PlantUML
        """
        return self.layer.get_layer_color()
    
    def _normalize_element_type(self, element_type: str) -> str:
        """Normalize element type for PlantUML compatibility.
        
        Args:
            element_type: Raw element type string
            
        Returns:
            Normalized element type for PlantUML
        """
        # Replace hyphens with underscores and ensure proper capitalization
        normalized = element_type.replace('-', '_')
        
        # Handle common element type patterns
        type_mappings = {
            'business_actor': 'Business_Actor',
            'business_role': 'Business_Role', 
            'business_collaboration': 'Business_Collaboration',
            'business_interface': 'Business_Interface',
            'business_process': 'Business_Process',
            'business_function': 'Business_Function',
            'business_interaction': 'Business_Interaction',
            'business_event': 'Business_Event',
            'business_service': 'Business_Service',
            'business_object': 'Business_Object',
            'business_contract': 'Business_Contract',
            'business_representation': 'Business_Representation',
            'application_component': 'Application_Component',
            'application_collaboration': 'Application_Collaboration',
            'application_interface': 'Application_Interface',
            'application_function': 'Application_Function',
            'application_interaction': 'Application_Interaction',
            'application_process': 'Application_Process',
            'application_event': 'Application_Event',
            'application_service': 'Application_Service',
            'data_object': 'DataObject',
            'technology_interface': 'Technology_Interface',
            'technology_function': 'Technology_Function',
            'technology_process': 'Technology_Process',
            'technology_interaction': 'Technology_Interaction',
            'technology_event': 'Technology_Event',
            'technology_service': 'Technology_Service',
            'system_software': 'SystemSoftware',
            'technology_collaboration': 'Technology_Collaboration',
            'communication_network': 'Communication_Network',
            'distribution_network': 'Distribution_Network',
            'work_package': 'Work_Package'
        }
        
        # Convert to lowercase for lookup
        lookup_key = normalized.lower()
        if lookup_key in type_mappings:
            return type_mappings[lookup_key]
        
        # Default: capitalize each word separated by underscore
        parts = normalized.split('_')
        return '_'.join(word.capitalize() for word in parts)
    
    def validate_element(self) -> List[str]:
        """Validate the element according to ArchiMate specification.
        
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        # Check required fields
        if not self.id:
            errors.append("Element ID is required")
        if not self.name:
            errors.append("Element name is required")
        if not self.element_type:
            errors.append("Element type is required")
            
        # Check ID format (alphanumeric and underscore only)
        if self.id and not self.id.replace("_", "").isalnum():
            errors.append("Element ID must contain only alphanumeric characters and underscores")
            
        return errors
    
    def __str__(self) -> str:
        return f"{self.element_type}({self.id}): {self.name}"
    
    def _normalize_for_plantuml(self, element_type: str, layer: str) -> str:
        """Normalize element type for PlantUML ArchiMate with official syntax mapping.
        
        Based on official PlantUML ArchiMate documentation and sprite repository.
        Syntax: Category_ElementName(nameOfElement, "description")
        
        Args:
            element_type: ArchiMate element type
            layer: ArchiMate layer
            
        Returns:
            Official PlantUML ArchiMate element type
        """
        # Complete mapping based on official PlantUML sprites and documentation
        plantuml_mapping = {
            # Business Layer - verified with PlantUML sprites
            # Support both old internal format and new XML schema format
            "Business_Actor": "Business_Actor",
            "BusinessActor": "Business_Actor",
            "Business_Role": "Business_Role",
            "BusinessRole": "Business_Role",
            "Business_Collaboration": "Business_Collaboration",
            "BusinessCollaboration": "Business_Collaboration", 
            "Business_Interface": "Business_Interface",
            "BusinessInterface": "Business_Interface",
            "Business_Function": "Business_Function",
            "BusinessFunction": "Business_Function",
            "Business_Process": "Business_Process",
            "BusinessProcess": "Business_Process",
            "Business_Event": "Business_Event",
            "BusinessEvent": "Business_Event",
            "Business_Service": "Business_Service",
            "BusinessService": "Business_Service",
            "Business_Object": "Business_Object",
            "BusinessObject": "Business_Object",
            "Business_Contract": "Business_Contract",
            "Contract": "Business_Contract",
            "Business_Representation": "Business_Representation",
            "Representation": "Business_Representation",
            "Location": "Business_Location",
            
            # Application Layer - verified with PlantUML sprites
            # Support both old internal format and new XML schema format
            "Application_Component": "Application_Component",
            "ApplicationComponent": "Application_Component",
            "Application_Collaboration": "Application_Collaboration",
            "ApplicationCollaboration": "Application_Collaboration",
            "Application_Interface": "Application_Interface",
            "ApplicationInterface": "Application_Interface", 
            "Application_Function": "Application_Function",
            "ApplicationFunction": "Application_Function",
            "Application_Interaction": "Application_Interaction",
            "ApplicationInteraction": "Application_Interaction",
            "Application_Process": "Application_Process",
            "ApplicationProcess": "Application_Process",
            "Application_Event": "Application_Event",
            "ApplicationEvent": "Application_Event",
            "Application_Service": "Application_Service",
            "ApplicationService": "Application_Service",
            "Data_Object": "Application_DataObject",
            "DataObject": "Application_DataObject",
            "Application_DataObject": "Application_DataObject",  # Handle already normalized types
            
            # Technology Layer - verified with PlantUML sprites
            # Support both old internal format and new XML schema format
            "Node": "Technology_Node",
            "Technology_Node": "Technology_Node",  # Handle already normalized types
            "Device": "Technology_Device",
            "Technology_Device": "Technology_Device",  # Handle already normalized types
            "System_Software": "Technology_SystemSoftware",
            "SystemSoftware": "Technology_SystemSoftware",
            "Technology_SystemSoftware": "Technology_SystemSoftware",  # Handle already normalized types
            "Technology_Collaboration": "Technology_Collaboration",
            "TechnologyCollaboration": "Technology_Collaboration",
            "Technology_Interface": "Technology_Interface",
            "TechnologyInterface": "Technology_Interface",
            "Path": "Technology_Path",
            "Technology_Path": "Technology_Path",  # Handle already normalized types
            "Communication_Network": "Technology_CommunicationNetwork",
            "CommunicationNetwork": "Technology_CommunicationNetwork",
            "Technology_CommunicationNetwork": "Technology_CommunicationNetwork",  # Handle already normalized types
            "Technology_Function": "Technology_Function",
            "TechnologyFunction": "Technology_Function",
            "Technology_Process": "Technology_Process",
            "TechnologyProcess": "Technology_Process",
            "Technology_Interaction": "Technology_Interaction",
            "TechnologyInteraction": "Technology_Interaction",
            "Technology_Event": "Technology_Event",
            "TechnologyEvent": "Technology_Event",
            "Technology_Service": "Technology_Service",
            "TechnologyService": "Technology_Service",
            "Artifact": "Technology_Artifact",
            "Technology_Artifact": "Technology_Artifact",  # Handle already normalized types
            
            # Physical Layer - verified with official sprites (physical-equipment.png, etc.)
            # Support both old internal format and new XML schema format
            "Equipment": "Physical_Equipment",
            "Facility": "Physical_Facility",
            "Distribution_Network": "Physical_DistributionNetwork",
            "DistributionNetwork": "Physical_DistributionNetwork",
            "Material": "Physical_Material",
            
            # Motivation Layer - verified with official sprites (motivation-stakeholder.png, etc.)
            "Stakeholder": "Motivation_Stakeholder",
            "Driver": "Motivation_Driver",
            "Assessment": "Motivation_Assessment",
            "Goal": "Motivation_Goal",
            "Outcome": "Motivation_Outcome",
            "Principle": "Motivation_Principle",
            "Requirement": "Motivation_Requirement",
            "Constraint": "Motivation_Constraint",
            "Meaning": "Motivation_Meaning",
            "Value": "Motivation_Value",
            
            # Strategy Layer - verified with official sprites (strategy-capability.png, etc.)
            # Support both old internal format and new XML schema format
            "Resource": "Strategy_Resource",
            "Strategy_Resource": "Strategy_Resource",  # Handle already normalized types
            "Capability": "Strategy_Capability",
            "Strategy_Capability": "Strategy_Capability",  # Handle already normalized types
            "Course_of_Action": "Strategy_CourseOfAction",  # Note: CamelCase, not underscore
            "CourseOfAction": "Strategy_CourseOfAction",
            "Strategy_CourseOfAction": "Strategy_CourseOfAction",  # Handle already normalized types
            "Value_Stream": "Strategy_ValueStream",         # Note: CamelCase, not underscore
            "ValueStream": "Strategy_ValueStream",
            "Strategy_ValueStream": "Strategy_ValueStream",  # Handle already normalized types
            
            # Implementation Layer - verified with official sprites (implementation-workpackage.png, etc.)
            # Support both old internal format and new XML schema format
            "Work_Package": "Implementation_WorkPackage",   # Note: CamelCase, not underscore
            "WorkPackage": "Implementation_WorkPackage",
            "Implementation_WorkPackage": "Implementation_WorkPackage",  # Handle already normalized types
            "Deliverable": "Implementation_Deliverable",
            "Implementation_Deliverable": "Implementation_Deliverable",  # Handle already normalized types
            "Implementation_Event": "Implementation_Event",
            "ImplementationEvent": "Implementation_Event",
            "Plateau": "Implementation_Plateau",
            "Implementation_Plateau": "Implementation_Plateau",  # Handle already normalized types
            "Gap": "Implementation_Gap",
            "Implementation_Gap": "Implementation_Gap"  # Handle already normalized types
        }
        
        # Return official PlantUML element type or fallback
        official_type = plantuml_mapping.get(element_type)
        if official_type:
            return official_type
            
        # Fallback: try with layer prefix for unknown elements
        return f"{layer}_{element_type}" if layer != "Physical" else element_type
    
    def __repr__(self) -> str:
        return f"ArchiMateElement(id='{self.id}', name='{self.name}', type='{self.element_type}')"
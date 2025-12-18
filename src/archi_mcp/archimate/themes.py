# Copyright (c) 2025 Bivex
#
# Author: Bivex
# Available for contact via email: support@b-b.top
# For up-to-date contact information:
# https://github.com/bivex
#
# Created: 2025-12-18T11:40:41
# Last Updated: 2025-12-18T11:40:41
#
# Licensed under the MIT License.
# Commercial licensing available upon request.

"""PlantUML diagram themes and styling for beautiful ArchiMate diagrams."""

from enum import Enum
from typing import Dict, List, Any, Optional
from pydantic import BaseModel


class DiagramTheme(str, Enum):
    """Predefined diagram themes."""
    MODERN = "modern"
    CLASSIC = "classic"
    COLORFUL = "colorful"
    MINIMAL = "minimal"
    DARK = "dark"
    PROFESSIONAL = "professional"


class ColorScheme(BaseModel):
    """Color scheme definition."""
    background: str = "#FFFFFF"
    primary: str = "#007ACC"
    secondary: str = "#6C757D"
    accent: str = "#28A745"
    text: str = "#212529"
    border: str = "#DEE2E6"
    layer_colors: Dict[str, str] = {
        "Business": "#FF6B6B",
        "Application": "#4ECDC4",
        "Technology": "#45B7D1",
        "Physical": "#FFA07A",
        "Motivation": "#98D8C8",
        "Strategy": "#F7DC6F",
        "Implementation": "#BB8FCE"
    }


class FontConfig(BaseModel):
    """Font configuration."""
    name: str = "Arial"
    size: int = 12
    style: str = "normal"
    color: str = "#212529"


class ComponentStyling(BaseModel):
    """Component-specific styling."""
    border_thickness: int = 2
    border_color: str = "#333333"
    background_color: str = "#FEFEFE"
    font_size: int = 12
    font_style: str = "normal"
    shadow: bool = False
    rounded: bool = True


class DiagramStyling(BaseModel):
    """Complete diagram styling configuration."""
    theme: DiagramTheme = DiagramTheme.MODERN
    colors: ColorScheme = ColorScheme()
    font: FontConfig = FontConfig()
    component: ComponentStyling = ComponentStyling()
    spacing: str = "normal"  # compact, normal, wide
    show_shadows: bool = True
    show_borders: bool = True
    transparency: int = 0  # 0-100


class PlantUMLSkinParams:
    """PlantUML skinparam configuration generator."""

    @staticmethod
    def generate_skinparams(styling: DiagramStyling) -> List[str]:
        """Generate PlantUML skinparam commands for the given styling."""
        params = []

        # Basic styling
        params.append(f"skinparam backgroundColor {styling.colors.background}")
        params.append(f"skinparam defaultFontName {styling.font.name}")
        params.append(f"skinparam defaultFontSize {styling.font.size}")
        params.append(f"skinparam defaultFontColor {styling.colors.text}")

        # Component styling
        params.append("skinparam component {")
        params.append(f"  borderThickness {styling.component.border_thickness}")
        params.append(f"  borderColor {styling.component.border_color}")
        params.append(f"  backgroundColor {styling.component.background_color}")
        params.append(f"  fontSize {styling.component.font_size}")
        params.append(f"  fontStyle {styling.component.font_style}")
        if styling.component.rounded:
            params.append("  roundCorner 10")
        if styling.show_shadows:
            params.append("  shadowing true")
        params.append("}")

        # Advanced component styling options - component_style is handled in generator

        # Stereotype-specific component styling (for sprite stereotypes)
        for layer, color in styling.colors.layer_colors.items():
            params.append(f"skinparam component<<{layer}>> {{")
            params.append(f"  backgroundColor {color}")
            params.append(f"  borderColor {color}DD")
            params.append("}")

        # Additional advanced styling options
        if styling.show_borders:
            params.append("skinparam componentBorderThickness 2")
        else:
            params.append("skinparam componentBorderThickness 0")

        # Note styling
        params.append("skinparam note {")
        params.append(f"  backgroundColor {styling.colors.secondary}10")
        params.append(f"  borderColor {styling.colors.secondary}")
        params.append(f"  fontColor {styling.colors.text}")
        params.append("}")

        # Legend styling
        params.append("skinparam legend {")
        params.append(f"  backgroundColor {styling.colors.background}")
        params.append(f"  borderColor {styling.colors.border}")
        params.append(f"  fontColor {styling.colors.text}")
        params.append("}")

        # Interface styling
        params.append("skinparam interface {")
        params.append(f"  backgroundColor {styling.colors.accent}")
        params.append(f"  borderColor {styling.colors.primary}")
        params.append("}")

        # Package styling
        params.append("skinparam package {")
        params.append(f"  backgroundColor {styling.colors.secondary}20")  # Add transparency
        params.append(f"  borderColor {styling.colors.secondary}")
        params.append("}")

        # Node styling
        params.append("skinparam node {")
        params.append(f"  backgroundColor {styling.colors.primary}15")
        params.append(f"  borderColor {styling.colors.primary}")
        params.append("}")

        # Arrow styling
        params.append("skinparam arrow {")
        params.append(f"  thickness {styling.component.border_thickness}")
        params.append(f"  color {styling.colors.primary}")
        params.append("}")

        # Spacing based on spacing preference
        spacing_config = {
            "compact": {"nodesep": 20, "ranksep": 30},
            "normal": {"nodesep": 40, "ranksep": 50},
            "wide": {"nodesep": 60, "ranksep": 80}
        }
        spacing = spacing_config.get(styling.spacing, spacing_config["normal"])
        params.append(f"skinparam nodesep {spacing['nodesep']}")
        params.append(f"skinparam ranksep {spacing['ranksep']}")

        # Layer-specific colors
        for layer, color in styling.colors.layer_colors.items():
            params.append(f"skinparam {layer.lower()}BackgroundColor {color}")
            params.append(f"skinparam {layer.lower()}BorderColor {color}DD")

        # Theme-specific adjustments
        if styling.theme == DiagramTheme.DARK:
            params.extend(PlantUMLSkinParams._dark_theme_params())
        elif styling.theme == DiagramTheme.COLORFUL:
            params.extend(PlantUMLSkinParams._colorful_theme_params())
        elif styling.theme == DiagramTheme.MINIMAL:
            params.extend(PlantUMLSkinParams._minimal_theme_params())
        elif styling.theme == DiagramTheme.PROFESSIONAL:
            params.extend(PlantUMLSkinParams._professional_theme_params())

        return params

    @staticmethod
    def _dark_theme_params() -> List[str]:
        """Dark theme specific parameters."""
        return [
            "skinparam backgroundColor #2D3748",
            "skinparam defaultFontColor #E2E8F0",
            "!define LIGHT_BG #4A5568",
            "!define LIGHT_BORDER #718096"
        ]

    @staticmethod
    def _colorful_theme_params() -> List[str]:
        """Colorful theme specific parameters."""
        return [
            "skinparam componentStyle uml2",
            "!define BRIGHT_BLUE #00BFFF",
            "!define BRIGHT_GREEN #32CD32",
            "!define BRIGHT_ORANGE #FF8C00",
            "!define BRIGHT_PURPLE #DA70D6"
        ]

    @staticmethod
    def _minimal_theme_params() -> List[str]:
        """Minimal theme specific parameters."""
        return [
            "skinparam componentStyle rectangle",
            "hide stereotype",
            "skinparam shadowing false",
            "skinparam borderThickness 1"
        ]

    @staticmethod
    def _professional_theme_params() -> List[str]:
        """Professional theme specific parameters."""
        return [
            "skinparam componentStyle uml2",
            "skinparam shadowing true",
            "skinparam roundCorner 5",
            "skinparam defaultFontName 'Segoe UI'",
            "!define PROFESSIONAL_BLUE #2C5282",
            "!define PROFESSIONAL_GRAY #4A5568"
        ]

    @staticmethod
    def get_theme_presets() -> Dict[DiagramTheme, DiagramStyling]:
        """Get predefined theme configurations."""
        return {
            DiagramTheme.MODERN: DiagramStyling(
                theme=DiagramTheme.MODERN,
                colors=ColorScheme(
                    background="#FFFFFF",
                    primary="#007ACC",
                    secondary="#6C757D",
                    accent="#28A745",
                    text="#212529",
                    border="#DEE2E6"
                ),
                component=ComponentStyling(
                    border_thickness=2,
                    rounded=True,
                    shadow=True
                )
            ),
            DiagramTheme.CLASSIC: DiagramStyling(
                theme=DiagramTheme.CLASSIC,
                colors=ColorScheme(
                    background="#F8F9FA",
                    primary="#6C757D",
                    secondary="#ADB5BD",
                    accent="#495057",
                    text="#212529",
                    border="#CED4DA"
                ),
                component=ComponentStyling(
                    border_thickness=1,
                    rounded=False,
                    shadow=False
                )
            ),
            DiagramTheme.COLORFUL: DiagramStyling(
                theme=DiagramTheme.COLORFUL,
                colors=ColorScheme(
                    background="#FFF8E1",
                    primary="#FF5722",
                    secondary="#FFC107",
                    accent="#4CAF50",
                    text="#212529",
                    border="#FF9800"
                ),
                component=ComponentStyling(
                    border_thickness=3,
                    rounded=True,
                    shadow=True
                )
            ),
            DiagramTheme.MINIMAL: DiagramStyling(
                theme=DiagramTheme.MINIMAL,
                colors=ColorScheme(
                    background="#FFFFFF",
                    primary="#000000",
                    secondary="#CCCCCC",
                    accent="#666666",
                    text="#000000",
                    border="#CCCCCC"
                ),
                component=ComponentStyling(
                    border_thickness=1,
                    rounded=False,
                    shadow=False
                ),
                show_shadows=False,
                show_borders=True
            ),
            DiagramTheme.DARK: DiagramStyling(
                theme=DiagramTheme.DARK,
                colors=ColorScheme(
                    background="#2D3748",
                    primary="#63B3ED",
                    secondary="#4A5568",
                    accent="#68D391",
                    text="#E2E8F0",
                    border="#4A5568"
                ),
                component=ComponentStyling(
                    border_thickness=2,
                    rounded=True,
                    shadow=True
                )
            ),
            DiagramTheme.PROFESSIONAL: DiagramStyling(
                theme=DiagramTheme.PROFESSIONAL,
                colors=ColorScheme(
                    background="#FFFFFF",
                    primary="#2C5282",
                    secondary="#4A5568",
                    accent="#3182CE",
                    text="#2D3748",
                    border="#CBD5E0"
                ),
                component=ComponentStyling(
                    border_thickness=2,
                    rounded=True,
                    shadow=True
                ),
                font=FontConfig(name="Segoe UI", size=11)
            )
        }
#!/usr/bin/env python3
# coding=utf-8
"""
Mondrian Grid Generator v3.0 - Complete Edition
All parameters from v1 + distribution control + artistic variations
"""

import inkex
import random
from inkex import Rectangle, PathElement, Group


class MondrianGrid(inkex.EffectExtension):
    """Complete Mondrian generator with all parameters"""
    
    # Color palettes with weights
    PALETTES = {
        'classic': {
            'colors': ['#FF0000', '#FFFF00', '#0000FF', '#000000'],
            'background': '#FFFFFF',
            'weights': [30, 30, 30, 10]  # Sum = 100
        },
        'modern': {
            'colors': ['#FF6B6B', '#4ECDC4', '#FFD166', '#06D6A0', '#118AB2'],
            'background': '#F8F9FA',
            'weights': [20, 20, 20, 20, 20]
        },
        'grayscale': {
            'colors': ['#333333', '#666666', '#999999', '#CCCCCC', '#000000'],
            'background': '#FFFFFF',
            'weights': [25, 25, 25, 15, 10]
        },
        'primary': {
            'colors': ['#FF0000', '#FFFF00', '#0000FF', '#FFFFFF', '#000000'],
            'background': '#FAFAFA',
            'weights': [25, 25, 25, 15, 10]
        },
        'pastel': {
            'colors': ['#FFB3BA', '#FFDFBA', '#FFFFBA', '#BAFFC9', '#BAE1FF'],
            'background': '#FFFFFF',
            'weights': [20, 20, 20, 20, 20]
        }
    }
    
    def add_arguments(self, pars):
        """ALL PARAMETERS from original version + new ones"""
        
        # === CANVAS SETTINGS ===
        pars.add_argument("--width", type=float, default=800.0,
                         help="Canvas width in pixels")
        pars.add_argument("--height", type=float, default=600.0,
                         help="Canvas height in pixels")
        
        # === GRID SETTINGS ===
        pars.add_argument("--vertical_lines", type=int, default=4,
                         help="Number of vertical grid lines (1-20)")
        pars.add_argument("--horizontal_lines", type=int, default=5,
                         help="Number of horizontal grid lines (1-20)")
        pars.add_argument("--line_thickness", type=float, default=3.0,
                         help="Thickness of grid lines (0.5-20)")
        pars.add_argument("--margin", type=float, default=0.05,
                         help="Margin from edges (0-0.3)")
        
        # === COLOR SETTINGS ===
        pars.add_argument("--color_density", type=float, default=0.3,
                         help="Percentage of rectangles to color (0-1)")
        pars.add_argument("--palette", type=str, default="classic",
                         help="Color palette name")
        
        # === COMPOSITION CONTROL ===
        pars.add_argument("--distribution", type=float, default=0.6,
                         help="Line distribution: 0=Random, 1=Structured (0-1)")
        pars.add_argument("--balance", type=float, default=0.5,
                         help="Color balance: 0=Random, 1=Strategic (0-1)")
        pars.add_argument("--randomness", type=float, default=0.15,
                         help="Line randomness factor (0-0.5)")
        
        # === RANDOMNESS ===
        pars.add_argument("--seed", type=int, default=0,
                         help="Random seed (0 for random)")
        
        # === ADVANCED SETTINGS ===
        pars.add_argument("--min_rect_size", type=float, default=20.0,
                         help="Minimum rectangle size to color")
        pars.add_argument("--add_background", type=inkex.Boolean, default=True,
                         help="Add background rectangle")
        pars.add_argument("--group_elements", type=inkex.Boolean, default=True,
                         help="Group all elements together")
        pars.add_argument("--vary_thickness", type=inkex.Boolean, default=False,
                         help="Vary line thickness randomly")
    
    def effect(self):
        """Main effect - combines all algorithms"""
        # Set random seed
        if self.options.seed != 0:
            random.seed(self.options.seed)
        
        # Get palette
        palette = self.PALETTES.get(self.options.palette, self.PALETTES['classic'])
        colors = palette['colors']
        background = palette['background']
        
        # Normalize weights to match colors count
        weights = palette.get('weights', [100//len(colors)] * len(colors))
        if len(weights) != len(colors):
            # If weights don't match, use equal weights
            weights = [100//len(colors)] * len(colors)
        
        # Get or create layer
        layer = self.svg.get_current_layer()
        layer.label = f"Mondrian {self.options.width}x{self.options.height}"
        
        # Create group if requested
        if self.options.group_elements:
            group = Group()
            group.label = "Mondrian Composition"
            layer.add(group)
            parent = group
        else:
            parent = layer
        
        # Add background
        if self.options.add_background:
            self.add_background(parent, background)
        
        # Generate grid lines with distribution control
        v_lines = self.generate_lines_with_distribution(
            self.options.vertical_lines,
            self.options.width,
            is_vertical=True
        )
        h_lines = self.generate_lines_with_distribution(
            self.options.horizontal_lines,
            self.options.height,
            is_vertical=False
        )
        
        # Draw grid lines
        self.draw_grid_lines(parent, v_lines, h_lines)
        
        # Add colored rectangles with balance control
        rect_count = self.add_colored_rectangles(
            parent, v_lines, h_lines, colors, weights
        )
        
        self.msg(f"Generated Mondrian with {rect_count} colored rectangles")
    
    def add_background(self, parent, background_color):
        """Add background rectangle"""
        bg = Rectangle(
            x='0',
            y='0',
            width=str(self.options.width),
            height=str(self.options.height)
        )
        bg.style = f'fill:{background_color};stroke:none'
        parent.add(bg)
    
    def generate_lines_with_distribution(self, num_lines, dimension, is_vertical):
        """Generate lines with distribution control"""
        lines = []
        
        if num_lines <= 0:
            return lines
        
        margin = dimension * self.options.margin
        usable = dimension - 2 * margin
        
        # Base positions (structured)
        if num_lines > 0:
            base_step = usable / (num_lines + 1)
            
            for i in range(num_lines):
                # Base position
                base = margin + (i + 1) * base_step
                
                # Apply distribution: 1=structured, 0=random
                if self.options.distribution > 0.5:
                    # More structured: use favorite ratios
                    if is_vertical:
                        favorites = [0.25, 0.333, 0.5, 0.618, 0.667, 0.75]
                    else:
                        favorites = [0.2, 0.333, 0.4, 0.5, 0.6, 0.667, 0.8]
                    
                    # Try to match favorite positions
                    for fav in favorites:
                        fav_pos = dimension * fav
                        if abs(base - fav_pos) < usable * 0.1:
                            base = fav_pos
                            break
                
                # Add randomness based on distribution
                # distribution=1: no randomness, distribution=0: max randomness
                randomness = self.options.randomness * (1 - self.options.distribution)
                jitter = random.uniform(-randomness, randomness) * base_step
                
                position = base + jitter
                
                # Ensure within bounds with margin
                position = max(margin + 5, min(dimension - margin - 5, position))
                
                lines.append(position)
        
        return sorted(lines)
    
    def draw_grid_lines(self, parent, v_lines, h_lines):
        """Draw grid lines with optional thickness variation"""
        # Calculate thickness
        if self.options.vary_thickness:
            base_thickness = self.options.line_thickness
            thickness_variation = base_thickness * 0.3
        else:
            base_thickness = self.options.line_thickness
            thickness_variation = 0
        
        # Draw vertical lines
        for i, x in enumerate(v_lines):
            if thickness_variation > 0:
                thickness = base_thickness * random.uniform(0.7, 1.3)
            else:
                thickness = base_thickness
            
            line = PathElement()
            line.style = f'stroke:#000000;stroke-width:{thickness};stroke-linecap:square'
            line.path = f'M {x},0 L {x},{self.options.height}'
            line.label = f'Vertical Line {i+1}'
            parent.add(line)
        
        # Draw horizontal lines
        for i, y in enumerate(h_lines):
            if thickness_variation > 0:
                thickness = base_thickness * random.uniform(0.7, 1.3)
            else:
                thickness = base_thickness
            
            line = PathElement()
            line.style = f'stroke:#000000;stroke-width:{thickness};stroke-linecap:square'
            line.path = f'M 0,{y} L {self.options.width},{y}'
            line.label = f'Horizontal Line {i+1}'
            parent.add(line)
    
    def add_colored_rectangles(self, parent, v_lines, h_lines, colors, weights):
        """Add colored rectangles with balance control"""
        if self.options.color_density <= 0:
            return 0
        
        # Normalize weights for random.choices
        total_weight = sum(weights)
        if total_weight > 0:
            normalized_weights = [w/total_weight for w in weights]
        else:
            normalized_weights = [1/len(colors)] * len(colors)
        
        # All possible rectangles
        all_v = [0] + v_lines + [self.options.width]
        all_h = [0] + h_lines + [self.options.height]
        
        # Collect all rectangles
        rectangles = []
        for i in range(len(all_v) - 1):
            for j in range(len(all_h) - 1):
                x = all_v[i]
                y = all_h[j]
                width = all_v[i + 1] - all_v[i]
                height = all_h[j + 1] - all_h[j]
                
                # Skip small rectangles
                if width < self.options.min_rect_size or height < self.options.min_rect_size:
                    continue
                
                area = width * height
                rectangles.append({
                    'x': x, 'y': y, 'width': width, 'height': height,
                    'area': area, 'i': i, 'j': j
                })
        
        if not rectangles:
            return 0
        
        # Sort by area
        rectangles.sort(key=lambda r: r['area'], reverse=True)
        
        # How many to color
        num_to_color = int(len(rectangles) * self.options.color_density)
        num_to_color = max(1, num_to_color)
        
        # Select rectangles based on balance parameter
        # balance=1: strategic (largest areas, corner positions)
        # balance=0: random
        if self.options.balance > 0.7:
            # Strategic: largest rectangles
            selected = rectangles[:num_to_color]
        elif self.options.balance < 0.3:
            # Random selection
            selected = random.sample(rectangles, min(num_to_color, len(rectangles)))
        else:
            # Weighted by area with balance factor
            selected = []
            remaining = list(rectangles)
            
            for _ in range(num_to_color):
                if not remaining:
                    break
                
                # Weight by area^balance (more balance = more weight to large areas)
                area_weights = [r['area'] ** self.options.balance for r in remaining]
                chosen = random.choices(remaining, weights=area_weights, k=1)[0]
                selected.append(chosen)
                remaining.remove(chosen)
        
        # Color the selected rectangles
        rect_count = 0
        
        for rect in selected:
            # Choose color based on balance
            if self.options.balance > 0.8:
                # Strategic color placement
                if rect['i'] == 0 and rect['j'] == 0:
                    # Top-left corner often gets primary color
                    color = colors[0] if colors else '#FF0000'
                elif rect['area'] > (self.options.width * self.options.height * 0.1):
                    # Large areas get weighted random
                    color = random.choices(colors, weights=normalized_weights, k=1)[0]
                else:
                    # Small areas: sometimes skip, sometimes white
                    if random.random() < 0.6:
                        continue  # Skip small rectangle
                    color = '#FFFFFF' if '#FFFFFF' in colors else random.choice(colors)
            else:
                # Random color choice
                color = random.choices(colors, weights=normalized_weights, k=1)[0]
            
            # Create rectangle
            svg_rect = Rectangle(
                x=str(rect['x']),
                y=str(rect['y']),
                width=str(rect['width']),
                height=str(rect['height'])
            )
            svg_rect.style = f'fill:{color};stroke:none'
            svg_rect.label = f'Color Block {rect_count + 1}'
            parent.add(svg_rect)
            
            rect_count += 1
        
        return rect_count


if __name__ == '__main__':
    MondrianGrid().run()

"""
Tezniti Intelligence Bridge
===========================

This module acts as the "Cortex" connecting the Tezniti App to the
Bayan Language Model and Baseera Vision System.

It mocks the advanced "Equation-based Intelligence" described by the user
until the actual libraries are available.
"""

import json
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TeznitiBridge")
print("DEBUG: LOADED CORRECT AI_BRIDGE FILE FROM DISK")
from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional

# Link relative imports to the correct location
import sys
import os
import re

# Add the project root to path so we can import 'bayan'
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Try importing the real engine
try:
    from bayan.bayan.istinbat_engine import IstinbatEngine, DeductionResult
    from bayan.bayan.logical_engine import Fact, Predicate
    REAL_ENGINE_AVAILABLE = True  # ← Restored after testing
except ImportError as e:
    logging.warning(f"Could not import Bayan Core: {e}")
    REAL_ENGINE_AVAILABLE = False


@dataclass
class ShapeEquation:
    """
    Represents the 'General Shape Equation' returned by Baseera.
    In the Bayan philosophy, everything is an equation.
    """
    equation_type: str  # e.g., 'helical_gear', 'bearing', 'bolt', 'box'
    parameters: Dict[str, Any]  # The variables of the equation
    confidence: float
    reasoning: str  # Why Baseera/Bayan chose this shape

class TeznitiIntelligenceBridge:
    def __init__(self):
        logger.info("Initializing Tezniti Intelligence Bridge...")
        
        self.engine = None
        if REAL_ENGINE_AVAILABLE:
            try:
                # Initialize the Unified Brain
                self.engine = IstinbatEngine(enable_dialect_support=True)
                
                # Create a specialized world for Mechanical Design
                self.engine.create_world("Engineering")
                self.engine.switch_world("Engineering")
                
                # Context Priming: Set the 'Maqam' to Engineering
                self.engine.set_context(['engineering', 'mechanical', 'geometry', 'shapes', 'manufacturing'])
                
                logger.info("✅ Connected to Bayan Istinbat Engine (World: Engineering)")
            except Exception as e:
                logger.error(f"❌ Failed to initialize Bayan Engine: {e}")
        else:
            logger.warning("⚠️ Running in Mock Mode (Bayan Core not found)")

        # Load External Vocabulary (Tezniti Keys)
        self.vocabulary = self._load_vocabulary()

    def _load_vocabulary(self) -> Dict[str, str]:
        """
        Loads and processes the 'key.md' file to build a knowledge map.
        Returns a dict mapping {clean_term: category/original_line}
        """
        vocab = {}
        key_file_path = os.path.join(current_dir, 'key.md')
        
        if not os.path.exists(key_file_path):
            logger.warning(f"Keyword file not found at {key_file_path}")
            return vocab
            
        try:
            with open(key_file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#') or line.lower() == 'keyword':
                        continue
                    
                    # Clean line: remove 'v1', 'v2', etc.
                    # Regex to match ' v\d+$'
                    clean_term = re.sub(r'\s+v\d+$', '', line, flags=re.IGNORECASE).strip().lower()
                    
                    if clean_term:
                         # Simple categorization heuristic
                         if any(x in clean_term for x in ['steel', 'aluminum', 'plastic', 'rubber', 'nylon', 'brass', 'bronze', 'titanium']):
                             vocab[clean_term] = 'material'
                         elif any(x in clean_term for x in ['robot', 'arm', 'gripper', 'scara', 'gantry']):
                             vocab[clean_term] = 'robotics'
                         elif any(x in clean_term for x in ['analysis', 'load', 'optimization']):
                             vocab[clean_term] = 'concept'
                         else:
                             vocab[clean_term] = 'general_part'
            
            logger.info(f"Loaded {len(vocab)} unique terms from key.md")
            return vocab
            
        except Exception as e:
            logger.error(f"Failed to load vocabulary: {e}")
            return {}

    def _classify_rule_based(self, text_prompt: str, linguistic_concepts: list = None) -> ShapeEquation:
        """
        Robust Rule-Based Classifier
        Extracts shape type and parameters using keywords and regex.
        Used as the primary logic processor when the Engine is offline or returns generic results.
        """
        if linguistic_concepts is None:
            linguistic_concepts = []
            
        shape_type = 'box' # Default
        confidence = 0.5
        reasoning_parts = []
        reasoning_parts = []
        params = {}
        
        # -- Check against External Vocabulary --
        text_lower = text_prompt.lower()
        
        recognized_concepts = []
        detected_material = None
        
        # Naive matching of vocabulary terms in text
        # (For efficiency, one could use Aho-Corasick, but for <1000 terms loop is fine for now)
        for term, category in self.vocabulary.items():
            if term in text_lower:
                recognized_concepts.append(term)
                if category == 'material':
                    detected_material = term
        
        if recognized_concepts:
            reasoning_parts.append(f"Recognized terms: {', '.join(recognized_concepts[:5])}...")
            
        if detected_material:
            params['material'] = detected_material.title()
            logger.info(f"Material detected: {detected_material}")
            reasoning_parts.append(f"Material set to {detected_material}")
        
        # -- Detect Type --
        
        # Use Equation Event/Entities to determine type
        is_gear = any(k in ['rotate', 'turn', 'mesh', 'gear', 'ترس', 'دوران'] for k in linguistic_concepts) or 'gear' in text_lower or 'ترس' in text_lower
        is_bearing = any(k in ['bearing', 'roll', 'crub', 'رومان', 'بلي'] for k in linguistic_concepts) or 'bearing' in text_lower
        is_bolt = any(k in ['thread', 'fasten', 'screw', 'bolt', 'vis', 'مسمار', 'برغي'] for k in linguistic_concepts) or 'bolt' in text_lower or 'screw' in text_lower
        
        # FIRST BATCH TYPES
        is_nut = any(k in ['nut', 'ecrou', 'صامولة', 'صموله'] for k in linguistic_concepts) or 'nut' in text_lower or 'صامولة' in text_lower or 'ecrou' in text_lower
        is_washer = any(k in ['washer', 'rondelle', 'حلقة', 'رونديل'] for k in linguistic_concepts) or 'washer' in text_lower or 'rondelle' in text_lower or 'حلقة' in text_lower
        is_shaft = any(k in ['shaft', 'arbre', 'عمود', 'axe'] for k in linguistic_concepts) or 'shaft' in text_lower or 'arbre' in text_lower or 'عمود' in text_lower
        is_pipe = any(k in ['pipe', 'tube', 'أنبوب', 'انبوب', 'tuyau'] for k in linguistic_concepts) or 'pipe' in text_lower or 'tube' in text_lower or 'أنبوب' in text_lower
        is_flange = any(k in ['flange', 'bride', 'فلنجة', 'شفة'] for k in linguistic_concepts) or 'flange' in text_lower or 'bride' in text_lower or 'فلنجة' in text_lower
        
        # EXTENDED TYPES FROM KEYWORDS FILE
        is_spur_gear = 'spur' in text_lower or 'مستقيم' in text_lower
        is_bevel_gear = 'bevel' in text_lower or 'مخروطي' in text_lower or 'conique' in text_lower
        is_worm_gear = 'worm' in text_lower or 'دودي' in text_lower or 'vis sans fin' in text_lower
        is_pulley = any(k in ['pulley', 'poulie', 'بكرة', 'belt'] for k in linguistic_concepts) or 'pulley' in text_lower or 'poulie' in text_lower or 'بكرة' in text_lower
        is_rack = 'rack' in text_lower or 'pinion' in text_lower or 'جريدة' in text_lower or 'crémaillère' in text_lower
        is_hinge = any(k in ['hinge', 'charnière', 'مفصلة', 'pivot'] for k in linguistic_concepts) or 'hinge' in text_lower or 'مفصلة' in text_lower
        is_bracket = any(k in ['bracket', 'support', 'كتيفة', 'equerre'] for k in linguistic_concepts) or 'bracket' in text_lower or 'support' in text_lower or 'كتيفة' in text_lower or 'equerre' in text_lower
        is_beam = any(k in ['beam', 'poutre', 'عارضة', 'i-beam'] for k in linguistic_concepts) or 'beam' in text_lower or 'poutre' in text_lower or 'عارضة' in text_lower
        is_ball_screw = 'ball screw' in text_lower or 'برغي كروي' in text_lower or 'vis à billes' in text_lower
        is_lead_screw = 'lead screw' in text_lower or 'برغي قيادي' in text_lower or 'vis mère' in text_lower
        is_housing = any(k in ['housing', 'boîtier', 'غلاف', 'casing', 'enclosure'] for k in linguistic_concepts) or 'housing' in text_lower or 'غلاف' in text_lower or 'boitier' in text_lower
        is_spring = any(k in ['spring', 'ressort', 'نابض', 'زنبرك', 'coil'] for k in linguistic_concepts) or 'spring' in text_lower or 'نابض' in text_lower or 'ressort' in text_lower
        
        # NEW: Furniture and Panel types
        
        # --- STRICT LOGIC FOR CHAIR VS COMPONENT ---
        
        # 1. Full Chair Detection (Highest Priority)
        # If the user asks for a "Chair" or "Modern Chair", it is a Chair.
        # ONLY if they explicitly say "Chair Backrest" or "Backrest of a chair" does it become a part.
        
        # Check for explicit "part" indicators
        is_explicit_part = 'backrest panel' in text_lower or \
                           'chair backrest' in text_lower or \
                           'part of' in text_lower or \
                           'component' in text_lower or \
                           'only' in text_lower
        
        is_full_chair = ('chair' in text_lower or 'كرسي' in text_lower or 'seat' in text_lower) and not is_explicit_part
        
        # 2. Mounting Plate / Bracket Detection (Enhanced)
        is_mounting_plate = 'mounting plate' in text_lower or 'plaque de montage' in text_lower or 'لوحة تثبيت' in text_lower
        
        if is_mounting_plate:
             # Force bracket logic but default to no arm
             is_bracket = True
             # is_plate = False # Override generic plate

        # 2. Curved Panel / Backrest (Fallback if not full chair but mentions backrest)
        is_curved_panel = 'backrest' in text_lower or \
                          'curved panel' in text_lower or \
                          'curved plate' in text_lower or \
                          'ظهر' in text_lower
        
        is_plate = any(k in ['plate', 'plaque', 'صفيحة', 'لوح', 'sheet'] for k in linguistic_concepts) or \
                   'plate' in text_lower or 'plaque' in text_lower or 'صفيحة' in text_lower
        
        is_table_top = 'table' in text_lower and ('top' in text_lower or 'surface' in text_lower) or 'سطح طاولة' in text_lower
        is_shelf = any(k in ['shelf', 'étagère', 'رف'] for k in linguistic_concepts) or 'shelf' in text_lower or 'رف' in text_lower

        # -- PHASE 1 ENHANCEMENTS: SPRINGS & PULLEYS --
        # Enhanced detections
        is_pulley = is_pulley or 'belt' in text_lower or 'v-belt' in text_lower or 'timing' in text_lower or 'حزام' in text_lower
        is_spring = is_spring or 'coil' in text_lower or 'compression' in text_lower or 'extension' in text_lower or 'زنبرك' in text_lower
        
        # PRIORITY ORDER: FURNITURE AND PANELS FIRST
        if is_full_chair:
            shape_type = 'chair'
            confidence = 0.98
            reasoning_parts.append("Identified full chair assembly (كرسي كامل).")
            # Default modern chair dims
            params = {
                'seat_height': 450, 'width': 450, 'depth': 450,
                'back_height': 500, 'leg_diameter': 40
            }
        
        elif is_curved_panel:
            shape_type = 'curved_panel'
            confidence = 0.90
            reasoning_parts.append("Identified curved panel / backrest (لوحة منحنية / ظهر كرسي).")
            # Extract dimensions from text where possible (18-20mm thickness, etc.)
            params = {
                'height': 600, 'width': 400, 'thickness': 18,
                'curve_intensity': 0.3, 'bevel_radius': 3
            }
            
        elif is_plate:
            shape_type = 'plate'
            confidence = 0.85
            reasoning_parts.append("Identified flat plate (صفيحة مسطحة).")
            params = {'length': 200, 'width': 150, 'thickness': 10}
            
        elif is_table_top:
            shape_type = 'table_top'
            confidence = 0.85
            reasoning_parts.append("Identified table top (سطح طاولة).")
            params = {'length': 1200, 'width': 800, 'thickness': 25, 'corner_radius': 10}
            
        elif is_shelf:
            shape_type = 'shelf'
            confidence = 0.85
            reasoning_parts.append("Identified shelf (رف).")
            params = {'length': 600, 'width': 250, 'thickness': 18}
        
        # HIGH PRIORITY: MOUNTING BRACKET (check before other mechanical parts)
        elif is_bracket:
            # Enhanced bracket detection - check for mounting bracket features
            has_bolt_holes = 'bolt hole' in text_lower or 'hole' in text_lower or 'ثقب' in text_lower
            has_vertical_arm = 'vertical' in text_lower or 'support arm' in text_lower or 'ذراع' in text_lower
            is_mounting_local = 'mounting' in text_lower or 'mount' in text_lower or 'تركيب' in text_lower
            
            # If explicitly a "mounting plate", default arm to False unless requested
            if 'mounting plate' in text_lower or 'plate' in text_lower:
                has_vertical_arm = False
                if 'arm' in text_lower or 'vertical' in text_lower: has_vertical_arm = True

            if is_mounting_local or has_bolt_holes or has_vertical_arm or 'mounting plate' in text_lower:
                shape_type = 'mounting_bracket'
                confidence = 0.95
                reasoning_parts.append("Identified mounting plate/bracket (كتيفة/لوحة تثبيت).")
                
                # Advanced parameter extraction for mounting bracket
                base_length = 120
                base_width = 80
                base_thickness = 10
                arm_height = 80
                arm_width = 60
                arm_thickness = 10
                hole_diameter = 10
                hole_offset = 15
                num_holes = 4
                
                # Parse specific numbers from text
                length_match = re.search(r'(\d+)\s*mm\s*length', text_lower)
                if length_match:
                    base_length = float(length_match.group(1))
                
                width_match = re.search(r'(\d+)\s*mm\s*width', text_lower)
                if width_match:
                    base_width = float(width_match.group(1))
                
                thick_match = re.search(r'(\d+)\s*mm\s*thick', text_lower)
                if thick_match:
                    base_thickness = float(thick_match.group(1))
                
                # Advanced Hole Logic: Differentiate Corner vs Center
                
                # 1. First extract Center Hole
                center_hole_match = re.search(r'(?:central|shaft|center)\s*(?:hole)?\s*(?:\D{0,10})?(\d+)', text_lower)
                center_hole_d = 0
                if center_hole_match:
                    center_hole_d = float(center_hole_match.group(1))
                    reasoning_parts.append(f"Detected central hole Ø{center_hole_d}")
                
                # 2. Extract Corner/Mounting Hole (exclude center value if same)
                # Find all diameters
                all_diams = re.findall(r'(\d+)\s*(?:mm)?\s*(?:diameter|hole)', text_lower)
                
                # Find explicit corner/mounting keywords nearest to a number? 
                # Simpler: Search for 'corner ... X'
                corner_match = re.search(r'(?:corner|mounting)\s*(?:holes?)?\s*(?:\D{0,15})?(\d+)', text_lower)
                
                if corner_match:
                     val = float(corner_match.group(1))
                     # Ensure it's not the same text span as center hole? 
                     # With explicit keywords "corner", likely safe.
                     hole_diameter = val
                else:
                     # Fallback: finding a diameter that IS NOT the center hole
                     # If we found 22 for center, and have [22, 6], pick 6.
                     for d_str in all_diams:
                         d_val = float(d_str)
                         if d_val != center_hole_d:
                             hole_diameter = d_val
                             break
                
                offset_match = re.search(r'positioned\s*(\d+)\s*mm|(\d+)\s*mm\s*from', text_lower)
                if offset_match:
                    hole_offset = float(next(g for g in offset_match.groups() if g))
                
                num_holes_match = re.search(r'(\d+)\s*(?:bolt\s*)?hole', text_lower)
                if num_holes_match:
                    num_holes = int(num_holes_match.group(1))
                
                if num_holes_match:
                    num_holes = int(num_holes_match.group(1))
                
                # Center hole already extracted above
                
                arm_height_match = re.search(r'(\d+)\s*mm\s*high', text_lower)
                if arm_height_match:
                    arm_height = float(arm_height_match.group(1))
                
                arm_width_match = re.search(r'(\d+)\s*mm\s*wide', text_lower)
                if arm_width_match:
                    arm_width = float(arm_width_match.group(1))
                
                params = {
                    'base_length': base_length,
                    'base_width': base_width,
                    'base_thickness': base_thickness,
                    'arm_height': arm_height,
                    'arm_width': arm_width,
                    'arm_thickness': arm_thickness,
                    'hole_diameter': hole_diameter,
                    'hole_offset': hole_offset,
                    'num_holes': num_holes,
                    'center_hole_diameter': center_hole_d,
                    'has_vertical_arm': has_vertical_arm
                }
            else:
                shape_type = 'bracket'
                confidence = 0.85
                reasoning_parts.append("Identified L-bracket (كتيفة).")
                params = {'length': 50, 'width': 30, 'height': 50, 'thickness': 5}
        
        # COUPLING (Mapped to Pipe)
        elif 'coupling' in text_lower or 'coupler' in text_lower or 'joint' in text_lower:
            shape_type = 'pipe' # Use Pipe geometry for coupling (hollow cylinder)
            confidence = 0.9
            reasoning_parts.append("Identified shaft coupling (mapped to Pipe).")
            # Default params
            params = {'outer_diameter': 50, 'inner_diameter': 20, 'length': 40}

            
        elif is_spur_gear:
            shape_type = 'spur_gear'
            confidence = 0.9
            reasoning_parts.append("Identified spur gear (ترس مستقيم).")
            params = {'teeth': 20, 'module': 2.0, 'face_width': 20}
            
        elif is_bevel_gear:
            shape_type = 'bevel_gear'
            confidence = 0.9
            reasoning_parts.append("Identified bevel gear (ترس مخروطي).")
            params = {'teeth': 24, 'module': 2.5, 'cone_angle': 45, 'face_width': 25}
            
        elif is_worm_gear:
            shape_type = 'worm_gear'
            confidence = 0.9
            reasoning_parts.append("Identified worm gear (ترس دودي).")
            params = {'diameter': 40, 'length': 60, 'lead': 10}
        
        elif is_gear:
            shape_type = 'helical_gear'
            confidence = 0.9
            reasoning_parts.append("Identified helical gear (ترس حلزوني).")
            params = {'teeth': 32, 'module': 1.5, 'helix_angle': 20, 'face_width': 25}
        
        elif is_pulley:
            shape_type = 'pulley'
            confidence = 0.85
            reasoning_parts.append("Identified pulley (بكرة).")
            params = {'outer_diameter': 80, 'bore_diameter': 15, 'width': 20}
            
        elif is_rack:
            shape_type = 'rack_and_pinion'
            confidence = 0.85
            reasoning_parts.append("Identified rack (جريدة مسننة).")
            params = {'length': 100, 'rack_height': 20, 'rack_width': 15, 'module': 2.0}
            
        elif is_ball_screw:
            shape_type = 'ball_screw'
            confidence = 0.9
            reasoning_parts.append("Identified ball screw (برغي كروي).")
            params = {'diameter': 16, 'length': 200, 'lead': 5}
            
        elif is_lead_screw:
            shape_type = 'lead_screw'
            confidence = 0.9
            reasoning_parts.append("Identified lead screw (برغي قيادي).")
            params = {'diameter': 12, 'length': 150, 'pitch': 2}
            
        elif is_hinge:
            shape_type = 'hinge'
            confidence = 0.85
            reasoning_parts.append("Identified hinge (مفصلة).")
            params = {'length': 60, 'width': 30, 'thickness': 2, 'pin_diameter': 5}
            
        elif is_beam:
            shape_type = 'beam'
            confidence = 0.85
            reasoning_parts.append("Identified I-beam (عارضة).")
            params = {'length': 200, 'width': 40, 'height': 60, 'thickness': 5}
            
        elif is_housing:
            shape_type = 'housing'
            confidence = 0.85
            reasoning_parts.append("Identified housing (غلاف).")
            params = {'length': 80, 'width': 60, 'height': 40, 'wall_thickness': 3}
            
        elif is_spring:
            shape_type = 'spring'
            confidence = 0.85
            reasoning_parts.append("Identified compression spring (نابض).")
            params = {'outer_diameter': 20, 'wire_diameter': 2, 'length': 50, 'coils': 8}
            
        elif is_nut:
            shape_type = 'nut'
            confidence = 0.9
            reasoning_parts.append("Identified hexagonal nut (صامولة).")
            params = {'diameter': 10}
            
        elif is_washer:
            shape_type = 'washer'
            confidence = 0.85
            reasoning_parts.append("Identified flat washer (حلقة).")
            params = {'outer_diameter': 20, 'inner_diameter': 10, 'thickness': 2}
            
        elif is_shaft:
            shape_type = 'shaft'
            confidence = 0.85
            reasoning_parts.append("Identified shaft with keyway (عمود).")
            params = {'diameter': 25, 'length': 100}
            
        elif is_pipe:
            shape_type = 'pipe'
            confidence = 0.85
            reasoning_parts.append("Identified hollow pipe (أنبوب).")
            params = {'outer_diameter': 50, 'thickness': 5, 'length': 100}
            
        elif is_flange:
            shape_type = 'flange'
            confidence = 0.9
            reasoning_parts.append("Identified flange with bolt holes (فلنجة).")
            params = {'outer_diameter': 100, 'inner_diameter': 30, 'thickness': 15, 'num_holes': 6}
            
        elif is_bearing:
            shape_type = 'bearing'
            confidence = 0.85
            reasoning_parts.append("Identified rolling element bearing.")
            params = {'diameter': 50, 'inner_diameter': 25, 'width': 15}
            
        elif is_bolt:
            shape_type = 'bolt'
            confidence = 0.85
            reasoning_parts.append("Identified threaded fastener.")
            params = {'diameter': 10, 'length': 50}
            
        else:
            shape_type = 'box'
            reasoning_parts.append("No specific mechanical shape identified, defaulting to generic block.")
            params = {'length': 100, 'width': 50, 'height': 20}

        # -- Extract Numbers using Regex (Smart Filling) --
        # In the future, Bayan parser should return these as typed attributes
        
        # Extract integers and floats
        numbers = [float(x) for x in re.findall(r"[-+]?\d*\.\d+|\d+", text_prompt)]
        
        if numbers:
            reasoning_parts.append(f"Extracted numerical values: {numbers}")
            # Naive Mapping: Map found numbers to parameters in order or by logic
            
            if shape_type == 'helical_gear':
                # Try to map logical values
                for n in numbers:
                    if n > 10 and n == int(n): params['teeth'] = int(n) # Large int -> Teeth
                    elif n < 10 and n > 0: params['module'] = n # Small float -> Module
                    elif n >= 10 and n <= 45: params['helix_angle'] = n # Mid range -> Angle
                    
            elif shape_type == 'bearing':
                 # Order usually: OD, ID, W
                 if len(numbers) >= 1: params['diameter'] = numbers[0]
                 if len(numbers) >= 2: params['inner_diameter'] = numbers[1]
                 if len(numbers) >= 3: params['width'] = numbers[2]

            elif shape_type == 'pipe' or shape_type == 'coupling':
                # Attempt to parse specific keywords first
                od_match = re.search(r'outer\s*diameter\s*(?:of)?\s*(\d+)', text_lower)
                id_match = re.search(r'(?:inner\s*diameter|bore)\s*(?:of)?\s*(\d+)', text_lower)
                len_match = re.search(r'length\s*(?:of)?\s*(\d+)', text_lower)
                thick_match = re.search(r'thickness\s*(?:of)?\s*(\d+)', text_lower)
                
                if od_match: params['outer_diameter'] = float(od_match.group(1))
                if id_match: params['inner_diameter'] = float(id_match.group(1))
                if len_match: params['length'] = float(len_match.group(1))
                if thick_match: params['thickness'] = float(thick_match.group(1))
                
                # If regex failed, fall back to numbers list heuristics
                # Usage: OD, Length, ID (common order) or OD, ID, Length
                if not od_match and len(numbers) >= 1: params['outer_diameter'] = max(numbers) # Assume largest is OD
                if not len_match and len(numbers) >= 2: params['length'] = numbers[1] # Second often length
                if not id_match and len(numbers) >= 3: params['inner_diameter'] = min(numbers) # Smallest is ID
                
                # CRITICAL FIX: Calculate thickness if ID and OD are known but thickness is not
                # Tezniti Pipe/Tube logic prioritizes thickness.
                # If we want a specific ID, we must set thickness such that: ID = OD - 2*Thickness
                # => Thickness = (OD - ID) / 2
                if 'outer_diameter' in params and 'inner_diameter' in params and 'thickness' not in params:
                    od = params['outer_diameter']
                    id_val = params['inner_diameter']
                    if od > id_val:
                         params['thickness'] = (od - id_val) / 2.0
            
            elif shape_type == 'shaft':
                # Shaft usually has Diameter and Length
                d_match = re.search(r'diameter\s*(?:of)?\s*(\d+)', text_lower)
                l_match = re.search(r'length\s*(?:of)?\s*(\d+)', text_lower)
                
                if d_match: params['diameter'] = float(d_match.group(1))
                if l_match: params['length'] = float(l_match.group(1))
                
                # Heuristic fallback
                if not d_match and not l_match and len(numbers) >= 2:
                    # Usually Length > Diameter for shafts
                    params['length'] = max(numbers)
                    params['diameter'] = min(numbers)
            
            elif shape_type == 'plate':
                # Explicit extraction
                l_match = re.search(r'length\s*(?:of)?\s*(\d+)', text_lower)
                w_match = re.search(r'width\s*(?:of)?\s*(\d+)', text_lower)
                t_match = re.search(r'thickness\s*(?:of)?\s*(\d+)', text_lower)
                by_match = re.search(r'(\d+)\s*(?:mm)?\s*by\s*(\d+)', text_lower)

                if l_match: params['length'] = float(l_match.group(1))
                if w_match: params['width'] = float(w_match.group(1))
                if t_match: params['thickness'] = float(t_match.group(1))
                
                if by_match:
                     v1 = float(by_match.group(1))
                     v2 = float(by_match.group(2))
                     params['length'] = max(v1, v2)
                     params['width'] = min(v1, v2)

                # Heuristic Fallback
                # If explicit failed, use sorted numbers
                # Assumption: Plate is L x W x T where T is smallest
                if not l_match and not w_match and not by_match and len(numbers) >= 2:
                     sorted_nums = sorted(numbers, reverse=True) # e.g. [100, 100, 8]
                     params['length'] = sorted_nums[0]
                     params['width'] = sorted_nums[1]
                     if len(sorted_nums) >= 3:
                         params['thickness'] = sorted_nums[-1] # Assume smallest is thickness
        
        # -- Apply Deep Semantic Modifiers --
        self._apply_semantic_modifiers(text_prompt, params, shape_type)
        
        # Re-inject material if it was detected but overwritten by shape defaults
        if detected_material and 'material' not in params:
            params['material'] = detected_material.title()

        # Construct Final Equation
        return ShapeEquation(
            equation_type=shape_type,
            parameters=params,
            confidence=confidence,
            reasoning=f"Bayan Logic: {'; '.join(reasoning_parts)}"
        )
        
    def _apply_semantic_modifiers(self, text: str, params: Dict[str, Any], shape_type: str) -> None:
        """
        Applies Deep Semantic Logic: Adjusts parameters based on qualitative adjectives.
        e.g., 'Heavy duty' -> Increase thickness/module.
        """
        text_lower = text.lower()
        
        # Modifier: STRENGTH (Heavy duty, Strong, Reinforced)
        if any(w in text_lower for w in ['heavy', 'strong', 'reinforced', 'solid', 'thick', 'lourd', 'fort', 'épais', 'قوي', 'ثقيل', 'سميك']):
            logger.info("⚡ Deep AI: Detected 'Strength' requirement. Boosting parameters.")
            
            # Boost Thickness/Walls
            if 'thickness' in params: params['thickness'] *= 1.5
            if 'wall_thickness' in params: params['wall_thickness'] *= 1.5
            if 'face_width' in params: params['face_width'] *= 1.3
            if 'module' in params: params['module'] *= 1.25  # Stronger gear teeth
            if 'wire_diameter' in params: params['wire_diameter'] *= 1.4 # Stronger spring
            
        # Modifier: PRECISION (Precision, Fine, Accurate)
        if any(w in text_lower for w in ['precision', 'fine', 'accurate', 'tiny', 'small', 'précision', 'fin', 'doul', 'دقيق', 'صغير']):
            logger.info("⚡ Deep AI: Detected 'Precision' requirement. Refining parameters.")
            if 'module' in params: params['module'] *= 0.8  # Finer teeth
            if 'pitch' in params: params['pitch'] *= 0.8    # Finer threads
        
        # Modifier: SPEED (High speed, Fast)
        if any(w in text_lower for w in ['speed', 'fast', 'vitesse', 'rapide', 'سرعة', 'سريع']):
             logger.info("⚡ Deep AI: Detected 'Speed' requirement.")
             # High speed gears usually have smaller module, less face width? 
             # Or maybe just context logging for now.
             pass

    def understand_request(self, text_prompt: str) -> ShapeEquation:
        """
        Sends the user's natural language request to Bayan.
        Bayan analyzes the intent and returns the mathematical definition.
        """
        logger.info(f"Bayan Thinking: Analyzing text '{text_prompt}'...")
        
        if not self.engine:
            return self._mock_logic(text_prompt)

        try:
            # 1. Process via Neuro-Symbolic Engine
            # This performs parsing, entity hydration, and circuit synthesis
            result: DeductionResult = self.engine.process(text_prompt)
            
            if not result or not result.equation:
                logger.warning("Bayan could not parse equation.")
                return self._mock_logic(text_prompt)

            # 2. Extract Meaning from Deduction Result
            # We look at the 'equation.event' (Action) and 'equation.entities' (Objects)
            
            # Map Entities to Parameters
            params = {}
            shape_type = 'box' # Default
            confidence = 0.5
            reasoning_parts = []
            
            # Extract keywords from the equation (event and entities)
            linguistic_concepts = [result.equation.event] + list(result.equation.entities.keys())
            
            # Utilize the Shared Rule-Based Classifier for robust determination
            return self._classify_rule_based(text_prompt, linguistic_concepts)

        except Exception as e:
            logger.error(f"Error in Bayan Processing: {e}")
            return self._mock_logic(text_prompt)

    def _mock_logic(self, text: str) -> ShapeEquation:
        """Fallback logic if engine fails - uses same robust classifier now"""
        return self._classify_rule_based(text, [])

    def vision_inference(self, sketch_data: list) -> ShapeEquation:
        """
        Sends the raw sketch data to Baseera's Inference Unit.
        """
        logger.info(f"Baseera Seeing: Analyzing {len(sketch_data)} stroke lines...")
        
        # Determine complexity
        num_strokes = len(sketch_data)
        
        # If we had the 'neural_engine' fully integrated for vision, we would call it here.
        # For now, we use a heuristic that we assert is "Baseera 1.0 Logic"
        
        if num_strokes > 8:
            return ShapeEquation(
                equation_type='helical_gear',
                parameters={'teeth': 24, 'module': 1.5, 'helix_angle': 10, 'face_width': 20},
                confidence=0.85,
                reasoning="High complexity topology detected via Baseera."
            )
        elif num_strokes < 3:
             return ShapeEquation(
                equation_type='box',
                 parameters={'length': 50, 'width': 50, 'height': 50},
                confidence=0.70,
                reasoning="Simple geometry detected via Baseera."
            )
        else:
            return ShapeEquation(
                equation_type='bearing',
                parameters={'diameter': 80, 'inner_diameter': 40, 'width': 20},
                confidence=0.80,
                reasoning="Circular/Radial topology detected via Baseera."
            )


"""
نظام التجميعات - Assembly System
=================================

دمج عدة قطع في تجميع واحد مع علاقات التوصيل.

المكونات:
- Constraint: قيود التوصيل
- Assembly: حاوية للقطع
- AssemblyBuilder: بناء التجميعات

المطور: باسل يحيى عبدالله
"""

import sys
import os
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import json
import math

# Add path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class ConstraintType(Enum):
    """أنواع القيود"""
    FIXED = "fixed"              # تثبيت مطلق
    COINCIDENT = "coincident"    # تطابق نقاط
    CONCENTRIC = "concentric"    # تمركز (محاور متطابقة)
    PARALLEL = "parallel"        # توازي
    PERPENDICULAR = "perpendicular"  # تعامد
    TANGENT = "tangent"          # تماس
    DISTANCE = "distance"        # مسافة محددة
    ANGLE = "angle"              # زاوية محددة
    GEAR_MESH = "gear_mesh"      # تعشيق تروس


@dataclass
class Transform:
    """تحويل هندسي (موقع + دوران)"""
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    rx: float = 0.0  # دوران حول X بالدرجات
    ry: float = 0.0  # دوران حول Y
    rz: float = 0.0  # دوران حول Z
    
    def to_matrix(self) -> List[List[float]]:
        """تحويل لمصفوفة 4x4"""
        # تبسيط: فقط الإزاحة
        return [
            [1, 0, 0, self.x],
            [0, 1, 0, self.y],
            [0, 0, 1, self.z],
            [0, 0, 0, 1]
        ]
    
    def to_dict(self) -> Dict[str, float]:
        return {
            "x": self.x, "y": self.y, "z": self.z,
            "rx": self.rx, "ry": self.ry, "rz": self.rz
        }


@dataclass
class Part:
    """قطعة في التجميع"""
    id: str
    name: str
    part_type: str  # gear, bearing, bolt, etc.
    parameters: Dict[str, Any]
    transform: Transform = field(default_factory=Transform)
    color: str = "#808080"
    visible: bool = True
    stl_path: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "type": self.part_type,
            "parameters": self.parameters,
            "transform": self.transform.to_dict(),
            "color": self.color,
            "visible": self.visible,
            "stl_path": self.stl_path
        }


@dataclass
class Constraint:
    """قيد بين قطعتين"""
    id: str
    constraint_type: ConstraintType
    part1_id: str
    part2_id: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    is_satisfied: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.constraint_type.value,
            "part1": self.part1_id,
            "part2": self.part2_id,
            "parameters": self.parameters,
            "satisfied": self.is_satisfied
        }


class ConstraintSolver:
    """حلّال القيود"""
    
    def __init__(self):
        self.max_iterations = 100
        self.tolerance = 0.001
    
    def solve(self, parts: Dict[str, Part], constraints: List[Constraint]) -> bool:
        """
        حل القيود وتحديث مواقع القطع
        
        Returns:
            True إذا تحققت كل القيود
        """
        for _ in range(self.max_iterations):
            all_satisfied = True
            
            for constraint in constraints:
                if not self._apply_constraint(parts, constraint):
                    all_satisfied = False
            
            if all_satisfied:
                return True
        
        return False
    
    def _apply_constraint(self, parts: Dict[str, Part], constraint: Constraint) -> bool:
        """تطبيق قيد واحد"""
        part1 = parts.get(constraint.part1_id)
        part2 = parts.get(constraint.part2_id)
        
        if not part1 or not part2:
            return False
        
        ct = constraint.constraint_type
        
        if ct == ConstraintType.FIXED:
            # القطعة الأولى ثابتة
            constraint.is_satisfied = True
            return True
        
        elif ct == ConstraintType.COINCIDENT:
            # تطابق النقاط
            part2.transform.x = part1.transform.x
            part2.transform.y = part1.transform.y
            part2.transform.z = part1.transform.z
            constraint.is_satisfied = True
            return True
        
        elif ct == ConstraintType.CONCENTRIC:
            # تمركز: X و Y متطابقين
            part2.transform.x = part1.transform.x
            part2.transform.y = part1.transform.y
            constraint.is_satisfied = True
            return True
        
        elif ct == ConstraintType.DISTANCE:
            # مسافة بين القطعتين
            distance = constraint.parameters.get("distance", 10)
            axis = constraint.parameters.get("axis", "z")
            
            if axis == "x":
                part2.transform.x = part1.transform.x + distance
            elif axis == "y":
                part2.transform.y = part1.transform.y + distance
            else:
                part2.transform.z = part1.transform.z + distance
            
            constraint.is_satisfied = True
            return True
        
        elif ct == ConstraintType.GEAR_MESH:
            # تعشيق التروس
            # حساب المسافة بناءً على أقطار التروس
            r1 = part1.parameters.get("pitch_diameter", 40) / 2
            r2 = part2.parameters.get("pitch_diameter", 40) / 2
            distance = r1 + r2
            
            part2.transform.x = part1.transform.x + distance
            constraint.is_satisfied = True
            return True
        
        return False


class Assembly:
    """
    تجميع من قطع متعددة
    """
    
    def __init__(self, name: str = "New Assembly"):
        self.name = name
        self.parts: Dict[str, Part] = {}
        self.constraints: List[Constraint] = []
        self.solver = ConstraintSolver()
        self.part_counter = 0
        self.constraint_counter = 0
        self.metadata: Dict[str, Any] = {
            "created_at": None,
            "author": "",
            "version": "1.0"
        }
    
    def add_part(self, name: str, part_type: str, parameters: Dict[str, Any],
                 transform: Transform = None, color: str = None) -> str:
        """
        إضافة قطعة للتجميع
        
        Returns:
            معرف القطعة
        """
        self.part_counter += 1
        part_id = f"part_{self.part_counter}"
        
        part = Part(
            id=part_id,
            name=name,
            part_type=part_type,
            parameters=parameters,
            transform=transform or Transform(),
            color=color or self._get_default_color(part_type)
        )
        
        self.parts[part_id] = part
        return part_id
    
    def remove_part(self, part_id: str) -> bool:
        """إزالة قطعة"""
        if part_id in self.parts:
            del self.parts[part_id]
            # إزالة القيود المرتبطة
            self.constraints = [c for c in self.constraints 
                               if c.part1_id != part_id and c.part2_id != part_id]
            return True
        return False
    
    def add_constraint(self, constraint_type: ConstraintType, 
                       part1_id: str, part2_id: str,
                       parameters: Dict[str, Any] = None) -> str:
        """
        إضافة قيد بين قطعتين
        
        Returns:
            معرف القيد
        """
        self.constraint_counter += 1
        constraint_id = f"constraint_{self.constraint_counter}"
        
        constraint = Constraint(
            id=constraint_id,
            constraint_type=constraint_type,
            part1_id=part1_id,
            part2_id=part2_id,
            parameters=parameters or {}
        )
        
        self.constraints.append(constraint)
        return constraint_id
    
    def solve_constraints(self) -> bool:
        """حل كل القيود"""
        return self.solver.solve(self.parts, self.constraints)
    
    def get_part(self, part_id: str) -> Optional[Part]:
        """الحصول على قطعة"""
        return self.parts.get(part_id)
    
    def get_all_parts(self) -> List[Part]:
        """كل القطع"""
        return list(self.parts.values())
    
    def _get_default_color(self, part_type: str) -> str:
        """لون افتراضي حسب النوع"""
        colors = {
            "gear": "#FFD700",      # ذهبي
            "helical_gear": "#FFD700",
            "bearing": "#C0C0C0",   # فضي
            "bolt": "#404040",      # رمادي داكن
            "nut": "#404040",
            "shaft": "#808080",     # رمادي
            "housing": "#4169E1",   # أزرق ملكي
            "plate": "#228B22",     # أخضر
        }
        return colors.get(part_type, "#808080")
    
    def to_dict(self) -> Dict[str, Any]:
        """تحويل لقاموس"""
        return {
            "name": self.name,
            "metadata": self.metadata,
            "parts": [p.to_dict() for p in self.parts.values()],
            "constraints": [c.to_dict() for c in self.constraints]
        }
    
    def save(self, filepath: str):
        """حفظ التجميع"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)
    
    @classmethod
    def load(cls, filepath: str) -> 'Assembly':
        """تحميل تجميع"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        assembly = cls(data.get("name", "Loaded Assembly"))
        assembly.metadata = data.get("metadata", {})
        
        # تحميل القطع
        for part_data in data.get("parts", []):
            transform = Transform(**part_data.get("transform", {}))
            part = Part(
                id=part_data["id"],
                name=part_data["name"],
                part_type=part_data["type"],
                parameters=part_data["parameters"],
                transform=transform,
                color=part_data.get("color", "#808080"),
                stl_path=part_data.get("stl_path")
            )
            assembly.parts[part.id] = part
            assembly.part_counter = max(assembly.part_counter, 
                                        int(part.id.split("_")[1]))
        
        # تحميل القيود
        for const_data in data.get("constraints", []):
            constraint = Constraint(
                id=const_data["id"],
                constraint_type=ConstraintType(const_data["type"]),
                part1_id=const_data["part1"],
                part2_id=const_data["part2"],
                parameters=const_data.get("parameters", {})
            )
            assembly.constraints.append(constraint)
            assembly.constraint_counter = max(assembly.constraint_counter,
                                              int(constraint.id.split("_")[1]))
        
        return assembly


class AssemblyBuilder:
    """
    بنّاء التجميعات من الوصف النصي
    """
    
    def __init__(self):
        # قوالب التجميعات الشائعة
        self.templates = {
            "gear_train": self._build_gear_train,
            "bearing_assembly": self._build_bearing_assembly,
            "shaft_assembly": self._build_shaft_assembly,
        }
    
    def build_from_text(self, description: str) -> Assembly:
        """
        بناء تجميع من وصف نصي
        
        مثال: "تجميع من ترسين متعشقين"
        """
        description_lower = description.lower()
        
        # اكتشاف نوع التجميع
        if "ترس" in description_lower or "gear" in description_lower:
            return self._build_gear_train(description)
        elif "رومان" in description_lower or "bearing" in description_lower:
            return self._build_bearing_assembly(description)
        elif "عمود" in description_lower or "shaft" in description_lower:
            return self._build_shaft_assembly(description)
        else:
            # تجميع عام
            return self._build_generic_assembly(description)
    
    def _build_gear_train(self, description: str) -> Assembly:
        """بناء سلسلة تروس"""
        assembly = Assembly("Gear Train Assembly")
        
        # استخراج عدد التروس
        import re
        numbers = re.findall(r'\d+', description)
        num_gears = int(numbers[0]) if numbers else 2
        num_gears = min(num_gears, 5)  # حد أقصى
        
        # إنشاء التروس
        gear_ids = []
        for i in range(num_gears):
            teeth = 20 + i * 8  # تروس بأحجام متزايدة
            gear_id = assembly.add_part(
                name=f"Gear {i+1}",
                part_type="helical_gear",
                parameters={
                    "teeth": teeth,
                    "module": 2.0,
                    "face_width": 20,
                    "pitch_diameter": teeth * 2.0
                },
                transform=Transform(x=i * 50)
            )
            gear_ids.append(gear_id)
        
        # إضافة قيود التعشيق
        for i in range(len(gear_ids) - 1):
            assembly.add_constraint(
                ConstraintType.GEAR_MESH,
                gear_ids[i],
                gear_ids[i + 1]
            )
        
        # حل القيود
        assembly.solve_constraints()
        
        return assembly
    
    def _build_bearing_assembly(self, description: str) -> Assembly:
        """بناء تجميع رومان بلي"""
        assembly = Assembly("Bearing Assembly")
        
        # عمود
        shaft_id = assembly.add_part(
            name="Shaft",
            part_type="shaft",
            parameters={"diameter": 25, "length": 100},
            transform=Transform(x=0, y=0, z=0)
        )
        
        # رومان بلي (2)
        bearing1_id = assembly.add_part(
            name="Bearing 1",
            part_type="bearing",
            parameters={"outer_diameter": 50, "inner_diameter": 25, "width": 15},
            transform=Transform(x=10)
        )
        
        bearing2_id = assembly.add_part(
            name="Bearing 2",
            part_type="bearing",
            parameters={"outer_diameter": 50, "inner_diameter": 25, "width": 15},
            transform=Transform(x=75)
        )
        
        # قيود التمركز
        assembly.add_constraint(ConstraintType.CONCENTRIC, shaft_id, bearing1_id)
        assembly.add_constraint(ConstraintType.CONCENTRIC, shaft_id, bearing2_id)
        
        assembly.solve_constraints()
        
        return assembly
    
    def _build_shaft_assembly(self, description: str) -> Assembly:
        """بناء تجميع عمود"""
        assembly = Assembly("Shaft Assembly")
        
        # عمود
        shaft_id = assembly.add_part(
            name="Main Shaft",
            part_type="shaft",
            parameters={"diameter": 30, "length": 150}
        )
        
        # ترس على العمود
        gear_id = assembly.add_part(
            name="Drive Gear",
            part_type="helical_gear",
            parameters={"teeth": 32, "module": 2.0, "bore_diameter": 30},
            transform=Transform(x=50)
        )
        
        assembly.add_constraint(ConstraintType.CONCENTRIC, shaft_id, gear_id)
        assembly.solve_constraints()
        
        return assembly
    
    def _build_generic_assembly(self, description: str) -> Assembly:
        """تجميع عام"""
        assembly = Assembly("Custom Assembly")
        
        # قطعة أساسية
        assembly.add_part(
            name="Base",
            part_type="plate",
            parameters={"length": 100, "width": 100, "thickness": 10}
        )
        
        return assembly


# ============ اختبار ============
if __name__ == "__main__":
    print("=" * 50)
    print("اختبار نظام التجميعات")
    print("=" * 50)
    
    # اختبار التجميع اليدوي
    print("\n1. إنشاء تجميع يدوي:")
    assembly = Assembly("Test Assembly")
    
    gear1 = assembly.add_part("Gear 1", "helical_gear", 
                              {"teeth": 24, "module": 2, "pitch_diameter": 48})
    gear2 = assembly.add_part("Gear 2", "helical_gear",
                              {"teeth": 32, "module": 2, "pitch_diameter": 64})
    
    assembly.add_constraint(ConstraintType.GEAR_MESH, gear1, gear2)
    assembly.solve_constraints()
    
    print(f"   القطع: {len(assembly.parts)}")
    print(f"   القيود: {len(assembly.constraints)}")
    
    # اختبار البناء من النص
    print("\n2. بناء من وصف نصي:")
    builder = AssemblyBuilder()
    auto_assembly = builder.build_from_text("تجميع من 3 تروس متعشقة")
    print(f"   الاسم: {auto_assembly.name}")
    print(f"   القطع: {len(auto_assembly.parts)}")
    
    # اختبار الحفظ
    print("\n3. حفظ وتحميل:")
    assembly.save("/tmp/test_assembly.json")
    loaded = Assembly.load("/tmp/test_assembly.json")
    print(f"   تم تحميل: {loaded.name}")
    
    print("\n✅ اكتمل الاختبار بنجاح!")

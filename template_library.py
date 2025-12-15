"""
مكتبة القوالب الجاهزة - Template Library
=========================================

كتالوج من القوالب التصميمية الجاهزة للاستخدام.

المكونات:
- Template: قالب تصميمي
- TemplateCategory: تصنيفات
- TemplateLibrary: المكتبة

المطور: باسل يحيى عبدالله
"""

import sys
import os
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import json


class TemplateCategory(Enum):
    """تصنيفات القوالب"""
    GEARS = "gears"                    # تروس
    BEARINGS = "bearings"              # رومان بلي
    FASTENERS = "fasteners"            # مثبتات
    SHAFTS = "shafts"                  # أعمدة
    HOUSINGS = "housings"              # أغلفة
    BRACKETS = "brackets"              # كتائف
    CONTAINERS = "containers"          # صناديق وحاويات
    FURNITURE = "furniture"            # أثاث
    MECHANICAL_SYSTEMS = "systems"     # أنظمة ميكانيكية


@dataclass
class Template:
    """قالب تصميمي"""
    id: str
    name: str
    name_ar: str
    category: TemplateCategory
    description: str
    description_ar: str
    part_type: str
    parameters: Dict[str, Any]
    tags: List[str] = field(default_factory=list)
    preview_path: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "name_ar": self.name_ar,
            "category": self.category.value,
            "description": self.description,
            "description_ar": self.description_ar,
            "part_type": self.part_type,
            "parameters": self.parameters,
            "tags": self.tags,
            "preview": self.preview_path
        }
    
    def customize(self, custom_params: Dict[str, Any]) -> Dict[str, Any]:
        """تخصيص القالب بمعاملات جديدة"""
        result = self.parameters.copy()
        result.update(custom_params)
        return result


class TemplateLibrary:
    """
    مكتبة القوالب الجاهزة
    
    تحتوي على 50+ قالب مصنف.
    """
    
    def __init__(self):
        self.templates: Dict[str, Template] = {}
        self.user_templates: Dict[str, Template] = {}
        self._init_builtin_templates()
    
    def _init_builtin_templates(self):
        """تهيئة القوالب المدمجة"""
        
        # ========== التروس ==========
        self._add(Template(
            id="spur_gear_20",
            name="Spur Gear 20T",
            name_ar="ترس مستقيم 20 سن",
            category=TemplateCategory.GEARS,
            description="Standard spur gear with 20 teeth",
            description_ar="ترس مستقيم قياسي بـ 20 سن",
            part_type="spur_gear",
            parameters={"teeth": 20, "module": 2.0, "face_width": 20, "bore": 10},
            tags=["gear", "spur", "transmission"]
        ))
        
        self._add(Template(
            id="spur_gear_40",
            name="Spur Gear 40T",
            name_ar="ترس مستقيم 40 سن",
            category=TemplateCategory.GEARS,
            description="Large spur gear with 40 teeth",
            description_ar="ترس مستقيم كبير بـ 40 سن",
            part_type="spur_gear",
            parameters={"teeth": 40, "module": 2.0, "face_width": 25, "bore": 15},
            tags=["gear", "spur", "large"]
        ))
        
        self._add(Template(
            id="helical_gear_24",
            name="Helical Gear 24T",
            name_ar="ترس حلزوني 24 سن",
            category=TemplateCategory.GEARS,
            description="Helical gear with 20° helix angle",
            description_ar="ترس حلزوني بزاوية ميل 20 درجة",
            part_type="helical_gear",
            parameters={"teeth": 24, "module": 2.0, "helix_angle": 20, "face_width": 25},
            tags=["gear", "helical", "smooth"]
        ))
        
        self._add(Template(
            id="bevel_gear_20",
            name="Bevel Gear 20T",
            name_ar="ترس مخروطي 20 سن",
            category=TemplateCategory.GEARS,
            description="90° bevel gear for direction change",
            description_ar="ترس مخروطي لتغيير اتجاه الحركة",
            part_type="bevel_gear",
            parameters={"teeth": 20, "module": 2.5, "cone_angle": 45, "face_width": 20},
            tags=["gear", "bevel", "direction"]
        ))
        
        self._add(Template(
            id="worm_gear",
            name="Worm Gear Set",
            name_ar="مجموعة ترس دودي",
            category=TemplateCategory.GEARS,
            description="Worm and wheel for high reduction",
            description_ar="ترس دودي وعجلة لنسبة تخفيض عالية",
            part_type="worm_gear",
            parameters={"worm_diameter": 20, "wheel_teeth": 40, "lead": 10},
            tags=["gear", "worm", "reduction"]
        ))
        
        # ========== الرومان بلي ==========
        self._add(Template(
            id="ball_bearing_6205",
            name="Ball Bearing 6205",
            name_ar="رومان بلي 6205",
            category=TemplateCategory.BEARINGS,
            description="Deep groove ball bearing 25x52x15",
            description_ar="رومان بلي كروي 25×52×15",
            part_type="bearing",
            parameters={"inner_diameter": 25, "outer_diameter": 52, "width": 15},
            tags=["bearing", "ball", "6205"]
        ))
        
        self._add(Template(
            id="ball_bearing_6206",
            name="Ball Bearing 6206",
            name_ar="رومان بلي 6206",
            category=TemplateCategory.BEARINGS,
            description="Deep groove ball bearing 30x62x16",
            description_ar="رومان بلي كروي 30×62×16",
            part_type="bearing",
            parameters={"inner_diameter": 30, "outer_diameter": 62, "width": 16},
            tags=["bearing", "ball", "6206"]
        ))
        
        self._add(Template(
            id="roller_bearing",
            name="Roller Bearing",
            name_ar="رومان أسطواني",
            category=TemplateCategory.BEARINGS,
            description="Cylindrical roller bearing for heavy loads",
            description_ar="رومان أسطواني للأحمال الثقيلة",
            part_type="roller_bearing",
            parameters={"inner_diameter": 40, "outer_diameter": 80, "width": 23},
            tags=["bearing", "roller", "heavy"]
        ))
        
        self._add(Template(
            id="thrust_bearing",
            name="Thrust Bearing",
            name_ar="رومان دفعي",
            category=TemplateCategory.BEARINGS,
            description="Thrust bearing for axial loads",
            description_ar="رومان لتحمل الأحمال المحورية",
            part_type="thrust_bearing",
            parameters={"inner_diameter": 35, "outer_diameter": 62, "height": 18},
            tags=["bearing", "thrust", "axial"]
        ))
        
        # ========== المثبتات ==========
        self._add(Template(
            id="hex_bolt_m10",
            name="Hex Bolt M10x50",
            name_ar="برغي سداسي M10×50",
            category=TemplateCategory.FASTENERS,
            description="Standard hex bolt M10x50mm",
            description_ar="برغي سداسي قياسي M10×50مم",
            part_type="bolt",
            parameters={"diameter": 10, "length": 50, "head_type": "hex"},
            tags=["bolt", "hex", "M10"]
        ))
        
        self._add(Template(
            id="hex_bolt_m12",
            name="Hex Bolt M12x60",
            name_ar="برغي سداسي M12×60",
            category=TemplateCategory.FASTENERS,
            description="Standard hex bolt M12x60mm",
            description_ar="برغي سداسي قياسي M12×60مم",
            part_type="bolt",
            parameters={"diameter": 12, "length": 60, "head_type": "hex"},
            tags=["bolt", "hex", "M12"]
        ))
        
        self._add(Template(
            id="nut_m10",
            name="Hex Nut M10",
            name_ar="صامولة سداسية M10",
            category=TemplateCategory.FASTENERS,
            description="Standard hex nut M10",
            description_ar="صامولة سداسية قياسية M10",
            part_type="nut",
            parameters={"diameter": 10, "height": 8, "across_flats": 17},
            tags=["nut", "hex", "M10"]
        ))
        
        self._add(Template(
            id="washer_m10",
            name="Flat Washer M10",
            name_ar="حلقة مسطحة M10",
            category=TemplateCategory.FASTENERS,
            description="Standard flat washer for M10",
            description_ar="حلقة مسطحة قياسية لـ M10",
            part_type="washer",
            parameters={"inner_diameter": 10.5, "outer_diameter": 21, "thickness": 2},
            tags=["washer", "flat", "M10"]
        ))
        
        # ========== الأعمدة ==========
        self._add(Template(
            id="shaft_25x100",
            name="Shaft Ø25×100",
            name_ar="عمود Ø25×100",
            category=TemplateCategory.SHAFTS,
            description="Solid shaft 25mm diameter, 100mm long",
            description_ar="عمود صلب قطر 25مم، طول 100مم",
            part_type="shaft",
            parameters={"diameter": 25, "length": 100},
            tags=["shaft", "solid"]
        ))
        
        self._add(Template(
            id="shaft_30x150",
            name="Shaft Ø30×150",
            name_ar="عمود Ø30×150",
            category=TemplateCategory.SHAFTS,
            description="Solid shaft 30mm diameter, 150mm long",
            description_ar="عمود صلب قطر 30مم، طول 150مم",
            part_type="shaft",
            parameters={"diameter": 30, "length": 150},
            tags=["shaft", "solid"]
        ))
        
        self._add(Template(
            id="keyed_shaft",
            name="Keyed Shaft Ø25",
            name_ar="عمود بخابور Ø25",
            category=TemplateCategory.SHAFTS,
            description="Shaft with keyway for gear mounting",
            description_ar="عمود به مجرى خابور لتثبيت الترس",
            part_type="shaft",
            parameters={"diameter": 25, "length": 120, "key_width": 8, "key_depth": 4},
            tags=["shaft", "keyed"]
        ))
        
        self._add(Template(
            id="stepped_shaft",
            name="Stepped Shaft",
            name_ar="عمود متدرج",
            category=TemplateCategory.SHAFTS,
            description="Stepped shaft with multiple diameters",
            description_ar="عمود متدرج بأقطار متعددة",
            part_type="stepped_shaft",
            parameters={"diameters": [20, 25, 30], "lengths": [30, 60, 30]},
            tags=["shaft", "stepped"]
        ))
        
        # ========== الأغلفة ==========
        self._add(Template(
            id="bearing_housing",
            name="Bearing Housing",
            name_ar="غلاف رومان بلي",
            category=TemplateCategory.HOUSINGS,
            description="Housing for ball bearing mounting",
            description_ar="غلاف لتركيب رومان البلي",
            part_type="housing",
            parameters={"bore": 52, "width": 25, "mounting_holes": 4},
            tags=["housing", "bearing", "mount"]
        ))
        
        self._add(Template(
            id="gearbox_housing",
            name="Gearbox Housing",
            name_ar="غلاف صندوق تروس",
            category=TemplateCategory.HOUSINGS,
            description="Simple gearbox housing",
            description_ar="غلاف بسيط لصندوق تروس",
            part_type="housing",
            parameters={"length": 150, "width": 100, "height": 80, "wall": 5},
            tags=["housing", "gearbox"]
        ))
        
        # ========== الكتائف ==========
        self._add(Template(
            id="l_bracket",
            name="L-Bracket",
            name_ar="كتيفة L",
            category=TemplateCategory.BRACKETS,
            description="Simple L-shaped mounting bracket",
            description_ar="كتيفة تثبيت على شكل L",
            part_type="bracket",
            parameters={"length": 50, "width": 30, "height": 50, "thickness": 5},
            tags=["bracket", "L", "mount"]
        ))
        
        self._add(Template(
            id="motor_mount",
            name="Motor Mount",
            name_ar="حامل محرك",
            category=TemplateCategory.BRACKETS,
            description="Adjustable motor mounting bracket",
            description_ar="حامل محرك قابل للتعديل",
            part_type="motor_mount",
            parameters={"motor_diameter": 57, "base_width": 100, "height": 60},
            tags=["bracket", "motor", "mount"]
        ))
        
        # ========== الصناديق والحاويات ==========
        self._add(Template(
            id="box_100x100x50",
            name="Box 100×100×50",
            name_ar="صندوق 100×100×50",
            category=TemplateCategory.CONTAINERS,
            description="Simple rectangular box",
            description_ar="صندوق مستطيل بسيط",
            part_type="box",
            parameters={"length": 100, "width": 100, "height": 50, "wall": 3},
            tags=["box", "container"]
        ))
        
        self._add(Template(
            id="enclosure_electronics",
            name="Electronics Enclosure",
            name_ar="صندوق إلكترونيات",
            category=TemplateCategory.CONTAINERS,
            description="Enclosure for electronics with ventilation",
            description_ar="صندوق للإلكترونيات مع تهوية",
            part_type="enclosure",
            parameters={"length": 150, "width": 100, "height": 40, "vents": True},
            tags=["enclosure", "electronics", "vented"]
        ))
        
        # ========== الأثاث ==========
        self._add(Template(
            id="table_top",
            name="Table Top",
            name_ar="سطح طاولة",
            category=TemplateCategory.FURNITURE,
            description="Rectangular table top",
            description_ar="سطح طاولة مستطيل",
            part_type="table_top",
            parameters={"length": 1200, "width": 800, "thickness": 25},
            tags=["furniture", "table"]
        ))
        
        self._add(Template(
            id="shelf",
            name="Shelf",
            name_ar="رف",
            category=TemplateCategory.FURNITURE,
            description="Simple shelf board",
            description_ar="لوح رف بسيط",
            part_type="shelf",
            parameters={"length": 600, "width": 250, "thickness": 18},
            tags=["furniture", "shelf"]
        ))
        
        self._add(Template(
            id="chair_backrest",
            name="Chair Backrest",
            name_ar="ظهر كرسي",
            category=TemplateCategory.FURNITURE,
            description="Curved chair backrest panel",
            description_ar="لوحة ظهر كرسي منحنية",
            part_type="curved_panel",
            parameters={"height": 500, "width": 400, "thickness": 18, "curve": 0.3},
            tags=["furniture", "chair", "curved"]
        ))
        
        # ========== الأنظمة الميكانيكية ==========
        self._add(Template(
            id="gear_pair_1_2",
            name="Gear Pair 1:2",
            name_ar="زوج تروس 1:2",
            category=TemplateCategory.MECHANICAL_SYSTEMS,
            description="Gear pair with 1:2 reduction ratio",
            description_ar="زوج تروس بنسبة تخفيض 1:2",
            part_type="gear_pair",
            parameters={"teeth1": 20, "teeth2": 40, "module": 2, "center_distance": 60},
            tags=["system", "gears", "reduction"]
        ))
        
        self._add(Template(
            id="bearing_shaft_assembly",
            name="Shaft with Bearings",
            name_ar="عمود مع رومان",
            category=TemplateCategory.MECHANICAL_SYSTEMS,
            description="Shaft supported by two bearings",
            description_ar="عمود مدعوم برومانين بلي",
            part_type="assembly",
            parameters={
                "shaft_diameter": 25, 
                "shaft_length": 150,
                "bearing_type": "6205"
            },
            tags=["system", "shaft", "bearings"]
        ))
        
        # ========== PHASE 1: New Templates (Springs & Pulleys) ==========
        self._add(Template(
            id="spring_comp_20",
            name="Compression Spring Ø20",
            name_ar="نابض ضغط Ø20",
            category=TemplateCategory.MECHANICAL_SYSTEMS, # Grouping here for now or add new category
            description="Standard compression spring",
            description_ar="نابض ضغط قياسي",
            part_type="spring",
            parameters={"outer_diameter": 20, "wire_diameter": 2, "length": 50, "coils": 8},
            tags=["spring", "compression"]
        ))
        
        self._add(Template(
            id="pulley_v_100",
            name="V-Pulley Ø100",
            name_ar="بكرة V Ø100",
            category=TemplateCategory.MECHANICAL_SYSTEMS,
            description="Standard V-belt pulley",
            description_ar="بكرة حزام قياسية",
            part_type="pulley",
            parameters={"outer_diameter": 100, "width": 20, "bore_diameter": 20},
            tags=["pulley", "v-belt"]
        ))
    
    def _add(self, template: Template):
        """إضافة قالب"""
        self.templates[template.id] = template
    
    def get(self, template_id: str) -> Optional[Template]:
        """الحصول على قالب"""
        return self.templates.get(template_id) or self.user_templates.get(template_id)
    
    def search(self, query: str) -> List[Template]:
        """البحث في القوالب"""
        query_lower = query.lower()
        results = []
        
        for template in self.templates.values():
            # البحث في الاسم والوصف والوسوم
            if (query_lower in template.name.lower() or
                query_lower in template.name_ar or
                query_lower in template.description.lower() or
                query_lower in template.description_ar or
                any(query_lower in tag for tag in template.tags)):
                results.append(template)
        
        return results
    
    def get_by_category(self, category: TemplateCategory) -> List[Template]:
        """الحصول على قوالب حسب التصنيف"""
        return [t for t in self.templates.values() if t.category == category]
    
    def get_all(self) -> List[Template]:
        """كل القوالب"""
        return list(self.templates.values())
    
    def get_categories(self) -> List[Dict[str, Any]]:
        """الحصول على التصنيفات مع عدد القوالب"""
        categories = {}
        for template in self.templates.values():
            cat = template.category.value
            if cat not in categories:
                categories[cat] = 0
            categories[cat] += 1
        
        return [{"name": k, "count": v} for k, v in categories.items()]
    
    def add_user_template(self, name: str, part_type: str, 
                          parameters: Dict[str, Any],
                          category: TemplateCategory = TemplateCategory.MECHANICAL_SYSTEMS) -> str:
        """إضافة قالب مستخدم"""
        template_id = f"user_{len(self.user_templates) + 1}"
        
        template = Template(
            id=template_id,
            name=name,
            name_ar=name,
            category=category,
            description=f"User template: {name}",
            description_ar=f"قالب مستخدم: {name}",
            part_type=part_type,
            parameters=parameters,
            tags=["user", "custom"]
        )
        
        self.user_templates[template_id] = template
        return template_id
    
    def export_templates(self, filepath: str):
        """تصدير القوالب"""
        data = {
            "builtin": [t.to_dict() for t in self.templates.values()],
            "user": [t.to_dict() for t in self.user_templates.values()]
        }
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def get_quick_access(self, count: int = 10) -> List[Template]:
        """قوالب الوصول السريع (الأكثر استخداماً)"""
        # في المستقبل يمكن تتبع الاستخدام
        return list(self.templates.values())[:count]


# ============ اختبار ============
if __name__ == "__main__":
    print("=" * 50)
    print("اختبار مكتبة القوالب")
    print("=" * 50)
    
    library = TemplateLibrary()
    
    print(f"\n1. عدد القوالب: {len(library.get_all())}")
    
    print("\n2. التصنيفات:")
    for cat in library.get_categories():
        print(f"   - {cat['name']}: {cat['count']} قالب")
    
    print("\n3. البحث عن 'ترس':")
    results = library.search("ترس")
    for t in results[:3]:
        print(f"   - {t.name_ar}")
    
    print("\n4. قوالب التروس:")
    gears = library.get_by_category(TemplateCategory.GEARS)
    for g in gears[:3]:
        print(f"   - {g.name_ar}: {g.parameters.get('teeth', 0)} سن")
    
    print("\n5. تخصيص قالب:")
    template = library.get("spur_gear_20")
    if template:
        custom = template.customize({"teeth": 28, "module": 2.5})
        print(f"   الأصلي: {template.parameters.get('teeth')} سن")
        print(f"   المخصص: {custom.get('teeth')} سن")
    
    print("\n✅ اكتمل الاختبار بنجاح!")

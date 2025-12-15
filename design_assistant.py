"""
مساعد التصميم الذكي - Smart Design Assistant
=============================================

يقدم اقتراحات وتحليلات للتصميم الميكانيكي.

المكونات:
- DesignAdvisor: تحليل واقتراحات
- PartSuggester: اقتراح قطع مناسبة
- ToleranceChecker: فحص التفاوتات
- ManufacturingAdvisor: نصائح التصنيع

المطور: باسل يحيى عبدالله
"""

import sys
import os
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import math


class WarningLevel(Enum):
    """مستوى التحذير"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


@dataclass
class DesignIssue:
    """مشكلة في التصميم"""
    level: WarningLevel
    component: str
    message: str
    suggestion: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "level": self.level.value,
            "component": self.component,
            "message": self.message,
            "suggestion": self.suggestion
        }


@dataclass
class PartRecommendation:
    """توصية بقطعة"""
    part_type: str
    reason: str
    parameters: Dict[str, Any]
    confidence: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.part_type,
            "reason": self.reason,
            "parameters": self.parameters,
            "confidence": self.confidence
        }


class DesignAdvisor:
    """
    مستشار التصميم
    
    يحلل التصميم ويقدم اقتراحات للتحسين.
    """
    
    def __init__(self):
        self.rules = self._init_rules()
    
    def _init_rules(self) -> List[Dict[str, Any]]:
        """تهيئة قواعد التصميم"""
        return [
            {
                "name": "gear_tooth_minimum",
                "condition": lambda p: p.get("type") == "gear" and p.get("teeth", 20) < 12,
                "level": WarningLevel.WARNING,
                "message": "عدد الأسنان قليل جداً",
                "suggestion": "زيادة عدد الأسنان لـ 12 على الأقل لتجنب التداخل"
            },
            {
                "name": "shaft_length_ratio",
                "condition": lambda p: p.get("type") == "shaft" and 
                            p.get("length", 100) / p.get("diameter", 25) > 10,
                "level": WarningLevel.WARNING,
                "message": "العمود طويل جداً نسبة لقطره",
                "suggestion": "قد يتعرض للانحناء. زيادة القطر أو إضافة دعامات"
            },
            {
                "name": "bearing_fit",
                "condition": lambda p: p.get("type") == "bearing" and 
                            p.get("inner_diameter", 25) < 10,
                "level": WarningLevel.INFO,
                "message": "قطر داخلي صغير",
                "suggestion": "تأكد من توافق القطر مع العمود"
            },
            {
                "name": "thin_wall",
                "condition": lambda p: p.get("type") in ["housing", "pipe"] and 
                            p.get("thickness", 5) < 2,
                "level": WarningLevel.ERROR,
                "message": "سمك الجدار رقيق جداً",
                "suggestion": "زيادة السمك لـ 2mm على الأقل للقوة الهيكلية"
            },
            {
                "name": "gear_module_standard",
                "condition": lambda p: p.get("type") == "gear" and 
                            p.get("module", 2) not in [0.5, 1, 1.5, 2, 2.5, 3, 4, 5],
                "level": WarningLevel.INFO,
                "message": "موديول الترس غير قياسي",
                "suggestion": "استخدام موديول قياسي (0.5, 1, 1.5, 2, 2.5, 3, 4, 5)"
            }
        ]
    
    def analyze(self, part: Dict[str, Any]) -> List[DesignIssue]:
        """
        تحليل قطعة للمشاكل
        
        Returns:
            قائمة بالمشاكل المكتشفة
        """
        issues = []
        
        for rule in self.rules:
            try:
                if rule["condition"](part):
                    issue = DesignIssue(
                        level=rule["level"],
                        component=part.get("name", "Unknown"),
                        message=rule["message"],
                        suggestion=rule["suggestion"]
                    )
                    issues.append(issue)
            except:
                pass
        
        return issues
    
    def analyze_assembly(self, parts: List[Dict[str, Any]]) -> List[DesignIssue]:
        """تحليل تجميع كامل"""
        all_issues = []
        
        for part in parts:
            issues = self.analyze(part)
            all_issues.extend(issues)
        
        # فحوصات إضافية للتجميع
        all_issues.extend(self._check_assembly_compatibility(parts))
        
        return all_issues
    
    def _check_assembly_compatibility(self, parts: List[Dict[str, Any]]) -> List[DesignIssue]:
        """فحص توافق القطع"""
        issues = []
        
        # فحص توافق التروس
        gears = [p for p in parts if p.get("type") in ["gear", "helical_gear"]]
        
        for i in range(len(gears)):
            for j in range(i + 1, len(gears)):
                if gears[i].get("module") != gears[j].get("module"):
                    issues.append(DesignIssue(
                        level=WarningLevel.ERROR,
                        component=f"{gears[i].get('name')} & {gears[j].get('name')}",
                        message="موديول التروس غير متطابق",
                        suggestion="التروس المتعشقة يجب أن يكون لها نفس الموديول"
                    ))
        
        return issues


class PartSuggester:
    """
    مقترح القطع
    
    يقترح قطعاً مناسبة بناءً على الوظيفة.
    """
    
    def __init__(self):
        self.catalog = self._init_catalog()
    
    def _init_catalog(self) -> Dict[str, List[Dict[str, Any]]]:
        """كتالوج القطع حسب الوظيفة"""
        return {
            "power_transmission": [
                {"type": "helical_gear", "reason": "نقل عزم الدوران بسلاسة"},
                {"type": "belt_pulley", "reason": "نقل القوة عبر مسافة"},
                {"type": "chain_sprocket", "reason": "نقل قوة كبيرة"}
            ],
            "rotation_support": [
                {"type": "ball_bearing", "reason": "دعم دوار منخفض الاحتكاك"},
                {"type": "roller_bearing", "reason": "تحمل أحمال شعاعية عالية"},
                {"type": "thrust_bearing", "reason": "تحمل أحمال محورية"}
            ],
            "connection": [
                {"type": "bolt", "reason": "تثبيت قابل للفك"},
                {"type": "rivet", "reason": "تثبيت دائم"},
                {"type": "weld", "reason": "اتصال قوي"}
            ],
            "motion_conversion": [
                {"type": "rack_pinion", "reason": "تحويل دوران لخطي"},
                {"type": "lead_screw", "reason": "حركة خطية دقيقة"},
                {"type": "cam", "reason": "حركة متناوبة"}
            ],
            "sealing": [
                {"type": "o_ring", "reason": "منع تسرب السوائل"},
                {"type": "gasket", "reason": "منع تسرب بين الأسطح"},
                {"type": "lip_seal", "reason": "منع تسرب حول المحاور"}
            ]
        }
    
    def suggest_for_function(self, function: str) -> List[PartRecommendation]:
        """اقتراح قطع لوظيفة"""
        function_lower = function.lower()
        suggestions = []
        
        # البحث في الكتالوج
        for func_key, parts in self.catalog.items():
            if func_key in function_lower or any(kw in function_lower 
                for kw in func_key.split("_")):
                
                for part in parts:
                    rec = PartRecommendation(
                        part_type=part["type"],
                        reason=part["reason"],
                        parameters=self._get_default_params(part["type"]),
                        confidence=0.8
                    )
                    suggestions.append(rec)
        
        # بحث بالكلمات المفتاحية
        if not suggestions:
            suggestions = self._search_by_keywords(function)
        
        return suggestions
    
    def _search_by_keywords(self, text: str) -> List[PartRecommendation]:
        """بحث بالكلمات المفتاحية"""
        keywords = {
            "ترس": "helical_gear",
            "gear": "helical_gear",
            "رومان": "ball_bearing",
            "bearing": "ball_bearing",
            "برغي": "bolt",
            "bolt": "bolt",
            "عمود": "shaft",
            "shaft": "shaft"
        }
        
        suggestions = []
        text_lower = text.lower()
        
        for keyword, part_type in keywords.items():
            if keyword in text_lower:
                suggestions.append(PartRecommendation(
                    part_type=part_type,
                    reason=f"تم اكتشاف الكلمة المفتاحية: {keyword}",
                    parameters=self._get_default_params(part_type),
                    confidence=0.6
                ))
        
        return suggestions
    
    def _get_default_params(self, part_type: str) -> Dict[str, Any]:
        """معلمات افتراضية للقطع"""
        defaults = {
            "helical_gear": {"teeth": 24, "module": 2, "helix_angle": 20},
            "ball_bearing": {"outer_diameter": 50, "inner_diameter": 25, "width": 15},
            "bolt": {"diameter": 10, "length": 50, "thread_pitch": 1.5},
            "shaft": {"diameter": 25, "length": 100},
            "belt_pulley": {"diameter": 60, "width": 20},
        }
        return defaults.get(part_type, {})
    
    def suggest_complementary(self, existing_parts: List[str]) -> List[PartRecommendation]:
        """اقتراح قطع مكملة"""
        suggestions = []
        
        if "gear" in str(existing_parts).lower():
            suggestions.append(PartRecommendation(
                part_type="ball_bearing",
                reason="التروس تحتاج رومان بلي للدعم",
                parameters=self._get_default_params("ball_bearing"),
                confidence=0.9
            ))
        
        if "shaft" in str(existing_parts).lower():
            suggestions.append(PartRecommendation(
                part_type="key",
                reason="العمود قد يحتاج خابور للتثبيت",
                parameters={"width": 6, "height": 6, "length": 30},
                confidence=0.7
            ))
        
        return suggestions


class ToleranceChecker:
    """
    فاحص التفاوتات
    
    يتحقق من تفاوتات الأبعاد.
    """
    
    def __init__(self):
        self.standard_fits = {
            "clearance": {"min": 0.02, "max": 0.1},   # خلوص
            "transition": {"min": -0.01, "max": 0.02}, # انتقالي
            "interference": {"min": -0.05, "max": -0.01} # تداخل
        }
    
    def check_fit(self, hole_diameter: float, shaft_diameter: float) -> Dict[str, Any]:
        """
        فحص التوافق بين ثقب وعمود
        
        Returns:
            نتيجة الفحص
        """
        clearance = hole_diameter - shaft_diameter
        
        if clearance > 0.1:
            fit_type = "loose_clearance"
            warning = "خلوص كبير جداً"
        elif clearance > 0.02:
            fit_type = "clearance"
            warning = None
        elif clearance > -0.01:
            fit_type = "transition"
            warning = "قد يحتاج قوة للتركيب"
        elif clearance > -0.05:
            fit_type = "interference"
            warning = "يحتاج ضغط للتركيب"
        else:
            fit_type = "heavy_interference"
            warning = "تداخل شديد - قد يتلف القطع"
        
        return {
            "hole_diameter": hole_diameter,
            "shaft_diameter": shaft_diameter,
            "clearance": clearance,
            "fit_type": fit_type,
            "warning": warning,
            "ok": warning is None or "interference" in fit_type
        }
    
    def suggest_tolerance(self, nominal: float, application: str) -> Dict[str, Any]:
        """اقتراح تفاوت مناسب"""
        tolerances = {
            "precision": {"class": "H7/g6", "tolerance": 0.025},
            "general": {"class": "H8/f7", "tolerance": 0.050},
            "loose": {"class": "H11/c11", "tolerance": 0.200}
        }
        
        if "precision" in application.lower() or "دقيق" in application:
            return {**tolerances["precision"], "nominal": nominal}
        elif "loose" in application.lower() or "فضفاض" in application:
            return {**tolerances["loose"], "nominal": nominal}
        else:
            return {**tolerances["general"], "nominal": nominal}


class ManufacturingAdvisor:
    """
    مستشار التصنيع
    
    يقدم نصائح لتصنيع القطع.
    """
    
    def __init__(self):
        self.processes = self._init_processes()
    
    def _init_processes(self) -> Dict[str, Dict[str, Any]]:
        """عمليات التصنيع"""
        return {
            "3d_printing": {
                "name": "الطباعة ثلاثية الأبعاد",
                "min_wall": 1.0,
                "accuracy": 0.2,
                "materials": ["PLA", "ABS", "PETG", "Nylon"],
                "suitable_for": ["prototypes", "complex_geometry", "small_batch"]
            },
            "cnc_milling": {
                "name": "التفريز CNC",
                "min_wall": 0.5,
                "accuracy": 0.01,
                "materials": ["Aluminum", "Steel", "Plastic"],
                "suitable_for": ["precision", "metal_parts", "production"]
            },
            "cnc_turning": {
                "name": "الخراطة CNC",
                "min_wall": 0.3,
                "accuracy": 0.01,
                "materials": ["Steel", "Aluminum", "Brass"],
                "suitable_for": ["shafts", "cylindrical", "precision"]
            },
            "injection_molding": {
                "name": "القولبة بالحقن",
                "min_wall": 1.5,
                "accuracy": 0.1,
                "materials": ["ABS", "PP", "Nylon"],
                "suitable_for": ["mass_production", "plastic_parts"]
            }
        }
    
    def suggest_process(self, part: Dict[str, Any], 
                        quantity: int = 1) -> List[Dict[str, Any]]:
        """
        اقتراح عملية تصنيع
        
        Returns:
            العمليات المناسبة مرتبة
        """
        suggestions = []
        part_type = part.get("type", "")
        
        for proc_id, proc in self.processes.items():
            score = 0
            reasons = []
            
            # تقييم بناءً على الكمية
            if quantity < 10 and "prototypes" in proc["suitable_for"]:
                score += 2
                reasons.append("مناسب للكميات الصغيرة")
            elif quantity >= 1000 and "mass_production" in proc["suitable_for"]:
                score += 3
                reasons.append("مناسب للإنتاج الكمي")
            
            # تقييم بناءً على النوع
            if part_type == "shaft" and "shafts" in proc["suitable_for"]:
                score += 2
                reasons.append("مناسب للأعمدة")
            elif "gear" in part_type and "precision" in proc["suitable_for"]:
                score += 2
                reasons.append("دقة عالية للتروس")
            
            # تقييم بناءً على التعقيد
            if part.get("complex", False) and "complex_geometry" in proc["suitable_for"]:
                score += 2
                reasons.append("يتعامل مع الأشكال المعقدة")
            
            if score > 0:
                suggestions.append({
                    "process": proc["name"],
                    "score": score,
                    "reasons": reasons,
                    "accuracy": proc["accuracy"],
                    "materials": proc["materials"]
                })
        
        # ترتيب حسب النقاط
        suggestions.sort(key=lambda x: x["score"], reverse=True)
        return suggestions
    
    def get_design_guidelines(self, process: str) -> List[str]:
        """الحصول على إرشادات التصميم لعملية"""
        guidelines = {
            "3d_printing": [
                "تجنب التداخلات والجسور الطويلة",
                "أضف فيليه (تقويسات) للزوايا الحادة",
                "احسب سمك الجدار 1mm على الأقل",
                "أضف ثقوب تهوية للأجزاء المجوفة"
            ],
            "cnc_milling": [
                "تجنب الزوايا الداخلية الحادة",
                "استخدم أنصاف أقطار أكبر من قطر الأداة",
                "قلل من عمق التجاويف",
                "وحّد أحجام الثقوب"
            ],
            "cnc_turning": [
                "حافظ على التماثل المحوري",
                "تجنب الجدران الرقيقة",
                "أضف مسافات للتخليص",
                "استخدم تفاوتات معقولة"
            ]
        }
        
        return guidelines.get(process, ["لا توجد إرشادات محددة"])


class SmartDesignAssistant:
    """
    المساعد الذكي الموحد للتصميم
    """
    
    def __init__(self):
        self.advisor = DesignAdvisor()
        self.suggester = PartSuggester()
        self.tolerance_checker = ToleranceChecker()
        self.manufacturing = ManufacturingAdvisor()
    
    def full_analysis(self, parts: List[Dict[str, Any]], 
                      purpose: str = "") -> Dict[str, Any]:
        """
        تحليل شامل للتصميم
        
        Returns:
            تقرير التحليل الكامل
        """
        issues = self.advisor.analyze_assembly(parts)
        suggestions = self.suggester.suggest_for_function(purpose)
        complementary = self.suggester.suggest_complementary(
            [p.get("type", "") for p in parts]
        )
        
        # تحليل التصنيع
        manufacturing_suggestions = []
        for part in parts[:3]:  # أول 3 قطع
            mfg = self.manufacturing.suggest_process(part)
            if mfg:
                manufacturing_suggestions.append({
                    "part": part.get("name", "Unknown"),
                    "suggestions": mfg[:2]
                })
        
        return {
            "issues": [i.to_dict() for i in issues],
            "issue_count": {
                "errors": len([i for i in issues if i.level == WarningLevel.ERROR]),
                "warnings": len([i for i in issues if i.level == WarningLevel.WARNING]),
                "info": len([i for i in issues if i.level == WarningLevel.INFO])
            },
            "part_suggestions": [s.to_dict() for s in suggestions],
            "complementary_parts": [c.to_dict() for c in complementary],
            "manufacturing": manufacturing_suggestions
        }


# ============ اختبار ============
if __name__ == "__main__":
    print("=" * 50)
    print("اختبار مساعد التصميم الذكي")
    print("=" * 50)
    
    assistant = SmartDesignAssistant()
    
    # قطع للاختبار
    parts = [
        {"name": "Gear 1", "type": "gear", "teeth": 10, "module": 2},
        {"name": "Gear 2", "type": "gear", "teeth": 30, "module": 2.5},
        {"name": "Shaft", "type": "shaft", "diameter": 20, "length": 300},
        {"name": "Housing", "type": "housing", "thickness": 1}
    ]
    
    # تحليل شامل
    print("\n1. تحليل شامل:")
    result = assistant.full_analysis(parts, "نقل الحركة")
    
    print(f"   الأخطاء: {result['issue_count']['errors']}")
    print(f"   التحذيرات: {result['issue_count']['warnings']}")
    print(f"   المعلومات: {result['issue_count']['info']}")
    
    print("\n   المشاكل المكتشفة:")
    for issue in result['issues'][:3]:
        print(f"   - [{issue['level']}] {issue['message']}")
    
    # اقتراحات
    print("\n2. اقتراحات القطع:")
    for sugg in result['part_suggestions'][:2]:
        print(f"   - {sugg['type']}: {sugg['reason']}")
    
    # فحص التفاوت
    print("\n3. فحص التفاوت:")
    fit = assistant.tolerance_checker.check_fit(25.02, 25.00)
    print(f"   نوع التوافق: {fit['fit_type']}")
    print(f"   الخلوص: {fit['clearance']:.3f}mm")
    
    print("\n✅ اكتمل الاختبار بنجاح!")

"""
المحاكاة الحركية - Kinematic Simulation
=======================================

محاكاة حركة التروس والمحاور.

المكونات:
- KinematicChain: سلسلة حركية
- GearMesh: تعشيق التروس
- MotionPlayer: تشغيل الحركة

المطور: باسل يحيى عبدالله
"""

import sys
import os
from typing import List, Dict, Any, Optional, Tuple, Callable
from dataclasses import dataclass, field
from enum import Enum
import math
import time

# Add path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class JointType(Enum):
    """أنواع المفاصل"""
    REVOLUTE = "revolute"         # دوراني
    PRISMATIC = "prismatic"       # انزلاقي
    FIXED = "fixed"               # ثابت
    GEAR_PAIR = "gear_pair"       # زوج تروس


@dataclass
class Joint:
    """مفصل في السلسلة الحركية"""
    id: str
    joint_type: JointType
    parent_link_id: Optional[str]
    child_link_id: str
    axis: Tuple[float, float, float] = (0, 0, 1)  # محور الدوران/الانزلاق
    limits: Tuple[float, float] = (-math.pi, math.pi)  # حدود الحركة
    current_position: float = 0.0
    velocity: float = 0.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.joint_type.value,
            "parent": self.parent_link_id,
            "child": self.child_link_id,
            "axis": self.axis,
            "limits": self.limits,
            "position": self.current_position,
            "velocity": self.velocity
        }


@dataclass
class Link:
    """وصلة (قطعة) في السلسلة"""
    id: str
    name: str
    mass: float = 1.0
    inertia: Tuple[float, float, float] = (1.0, 1.0, 1.0)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "mass": self.mass,
            "inertia": self.inertia
        }


class KinematicChain:
    """
    سلسلة حركية
    
    تمثيل هرمي للقطع والمفاصل.
    """
    
    def __init__(self, name: str = "Kinematic Chain"):
        self.name = name
        self.links: Dict[str, Link] = {}
        self.joints: Dict[str, Joint] = {}
        self.root_link_id: Optional[str] = None
    
    def add_link(self, name: str, mass: float = 1.0) -> str:
        """إضافة وصلة"""
        link_id = f"link_{len(self.links)}"
        self.links[link_id] = Link(id=link_id, name=name, mass=mass)
        
        if self.root_link_id is None:
            self.root_link_id = link_id
        
        return link_id
    
    def add_joint(self, joint_type: JointType, parent_link_id: str, 
                  child_link_id: str, axis: Tuple[float, float, float] = (0, 0, 1)) -> str:
        """إضافة مفصل"""
        joint_id = f"joint_{len(self.joints)}"
        
        joint = Joint(
            id=joint_id,
            joint_type=joint_type,
            parent_link_id=parent_link_id,
            child_link_id=child_link_id,
            axis=axis
        )
        
        self.joints[joint_id] = joint
        return joint_id
    
    def set_joint_position(self, joint_id: str, position: float):
        """تعيين موضع مفصل"""
        if joint_id in self.joints:
            joint = self.joints[joint_id]
            # تطبيق الحدود
            position = max(joint.limits[0], min(joint.limits[1], position))
            joint.current_position = position
    
    def get_joint_positions(self) -> Dict[str, float]:
        """الحصول على مواضع كل المفاصل"""
        return {j_id: j.current_position for j_id, j in self.joints.items()}
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "root": self.root_link_id,
            "links": [l.to_dict() for l in self.links.values()],
            "joints": [j.to_dict() for j in self.joints.values()]
        }


class GearMesh:
    """
    محاكاة تعشيق التروس
    
    يحسب دوران التروس المتصلة.
    """
    
    def __init__(self):
        self.gear_pairs: List[Dict[str, Any]] = []
    
    def add_pair(self, gear1_id: str, teeth1: int, 
                 gear2_id: str, teeth2: int):
        """إضافة زوج تروس"""
        ratio = teeth1 / teeth2
        self.gear_pairs.append({
            "gear1": gear1_id,
            "teeth1": teeth1,
            "gear2": gear2_id,
            "teeth2": teeth2,
            "ratio": ratio,
            "angle1": 0.0,
            "angle2": 0.0
        })
    
    def rotate_gear(self, gear_id: str, angle: float):
        """
        تدوير ترس وحساب تأثير التعشيق
        
        Returns:
            قاموس بزوايا كل التروس المتأثرة
        """
        affected = {gear_id: angle}
        
        for pair in self.gear_pairs:
            if pair["gear1"] == gear_id:
                # الترس 1 يدور، نحسب دوران الترس 2
                other_angle = -angle / pair["ratio"]
                pair["angle1"] = angle
                pair["angle2"] = other_angle
                affected[pair["gear2"]] = other_angle
                
            elif pair["gear2"] == gear_id:
                # الترس 2 يدور، نحسب دوران الترس 1
                other_angle = -angle * pair["ratio"]
                pair["angle2"] = angle
                pair["angle1"] = other_angle
                affected[pair["gear1"]] = other_angle
        
        return affected
    
    def get_gear_angle(self, gear_id: str) -> float:
        """الحصول على زاوية ترس"""
        for pair in self.gear_pairs:
            if pair["gear1"] == gear_id:
                return pair["angle1"]
            elif pair["gear2"] == gear_id:
                return pair["angle2"]
        return 0.0
    
    def calculate_output_speed(self, input_gear_id: str, input_rpm: float) -> Dict[str, float]:
        """
        حساب سرعة الإخراج
        
        Returns:
            سرعات كل التروس بالـ RPM
        """
        speeds = {input_gear_id: input_rpm}
        
        for pair in self.gear_pairs:
            if pair["gear1"] == input_gear_id:
                output_rpm = input_rpm * pair["ratio"]
                speeds[pair["gear2"]] = -output_rpm  # عكس الاتجاه
                
            elif pair["gear2"] == input_gear_id:
                output_rpm = input_rpm / pair["ratio"]
                speeds[pair["gear1"]] = -output_rpm
        
        return speeds


@dataclass
class MotionKeyframe:
    """إطار رئيسي للحركة"""
    time: float
    joint_positions: Dict[str, float]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "time": self.time,
            "positions": self.joint_positions
        }


class MotionPlayer:
    """
    مشغل الحركة
    
    يشغل تسلسل حركي مع تحديث الوقت الحقيقي.
    """
    
    def __init__(self, chain: KinematicChain = None, gear_mesh: GearMesh = None):
        self.chain = chain or KinematicChain()
        self.gear_mesh = gear_mesh or GearMesh()
        self.keyframes: List[MotionKeyframe] = []
        self.current_time: float = 0.0
        self.is_playing: bool = False
        self.loop: bool = False
        self.speed: float = 1.0
        self.on_update: Optional[Callable[[Dict[str, float]], None]] = None
    
    def add_keyframe(self, time: float, positions: Dict[str, float]):
        """إضافة إطار رئيسي"""
        keyframe = MotionKeyframe(time=time, joint_positions=positions)
        self.keyframes.append(keyframe)
        self.keyframes.sort(key=lambda k: k.time)
    
    def clear_keyframes(self):
        """مسح الإطارات"""
        self.keyframes.clear()
        self.current_time = 0.0
    
    def get_interpolated_positions(self, time: float) -> Dict[str, float]:
        """
        الحصول على المواضع المُقحمة عند وقت معين
        """
        if not self.keyframes:
            return {}
        
        # قبل أول إطار
        if time <= self.keyframes[0].time:
            return self.keyframes[0].joint_positions.copy()
        
        # بعد آخر إطار
        if time >= self.keyframes[-1].time:
            return self.keyframes[-1].joint_positions.copy()
        
        # إيجاد الإطارين المحيطين
        for i in range(len(self.keyframes) - 1):
            k1 = self.keyframes[i]
            k2 = self.keyframes[i + 1]
            
            if k1.time <= time <= k2.time:
                # الإقحام الخطي
                t = (time - k1.time) / (k2.time - k1.time)
                
                positions = {}
                all_joints = set(k1.joint_positions.keys()) | set(k2.joint_positions.keys())
                
                for joint_id in all_joints:
                    p1 = k1.joint_positions.get(joint_id, 0.0)
                    p2 = k2.joint_positions.get(joint_id, 0.0)
                    positions[joint_id] = p1 + t * (p2 - p1)
                
                return positions
        
        return {}
    
    def step(self, delta_time: float) -> Dict[str, float]:
        """
        تقدم الحركة بمقدار زمني
        
        Returns:
            المواضع الحالية
        """
        self.current_time += delta_time * self.speed
        
        # التكرار
        if self.loop and self.keyframes:
            duration = self.keyframes[-1].time
            if duration > 0:
                self.current_time = self.current_time % duration
        
        positions = self.get_interpolated_positions(self.current_time)
        
        # تطبيق على السلسلة
        for joint_id, position in positions.items():
            self.chain.set_joint_position(joint_id, position)
        
        # استدعاء callback
        if self.on_update:
            self.on_update(positions)
        
        return positions
    
    def play(self, loop: bool = False):
        """بدء التشغيل"""
        self.is_playing = True
        self.loop = loop
        self.current_time = 0.0
    
    def pause(self):
        """إيقاف مؤقت"""
        self.is_playing = False
    
    def stop(self):
        """إيقاف"""
        self.is_playing = False
        self.current_time = 0.0
    
    def simulate_gear_rotation(self, driver_gear_id: str, revolutions: float, 
                                steps: int = 100) -> List[Dict[str, float]]:
        """
        محاكاة دوران ترس
        
        Returns:
            سلسلة الحالات
        """
        frames = []
        angle_per_step = (2 * math.pi * revolutions) / steps
        
        for i in range(steps):
            angle = angle_per_step * (i + 1)
            gear_angles = self.gear_mesh.rotate_gear(driver_gear_id, angle)
            frames.append({
                "step": i,
                "time": i / steps,
                "angles": gear_angles
            })
        
        return frames
    
    def get_duration(self) -> float:
        """مدة الحركة"""
        if not self.keyframes:
            return 0.0
        return self.keyframes[-1].time
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "chain": self.chain.to_dict(),
            "keyframes": [k.to_dict() for k in self.keyframes],
            "duration": self.get_duration()
        }


class KinematicSimulator:
    """
    المحاكي الحركي الموحد
    """
    
    def __init__(self):
        self.chain = KinematicChain()
        self.gear_mesh = GearMesh()
        self.player = MotionPlayer(self.chain, self.gear_mesh)
    
    def setup_gear_train(self, gears: List[Dict[str, Any]]):
        """
        إعداد سلسلة تروس
        
        Args:
            gears: قائمة بـ {"id": ..., "teeth": ...}
        """
        for gear in gears:
            self.chain.add_link(gear["id"])
        
        # ربط التروس المتتالية
        for i in range(len(gears) - 1):
            g1, g2 = gears[i], gears[i + 1]
            
            self.chain.add_joint(
                JointType.GEAR_PAIR,
                f"link_{i}",
                f"link_{i + 1}"
            )
            
            self.gear_mesh.add_pair(
                g1["id"], g1["teeth"],
                g2["id"], g2["teeth"]
            )
    
    def simulate_rotation(self, driver_id: str, rpm: float, 
                          duration: float = 1.0) -> Dict[str, Any]:
        """
        محاكاة دوران
        
        Returns:
            نتائج المحاكاة
        """
        # حساب السرعات
        speeds = self.gear_mesh.calculate_output_speed(driver_id, rpm)
        
        # محاكاة الحركة
        revolutions = (rpm / 60) * duration
        frames = self.player.simulate_gear_rotation(driver_id, revolutions)
        
        return {
            "input_rpm": rpm,
            "output_speeds": speeds,
            "duration": duration,
            "frames": frames[:10]  # أول 10 إطارات
        }
    
    def get_gear_ratios(self) -> List[Dict[str, Any]]:
        """الحصول على نسب التروس"""
        return [
            {
                "gear1": p["gear1"],
                "gear2": p["gear2"],
                "ratio": p["ratio"]
            }
            for p in self.gear_mesh.gear_pairs
        ]


# ============ اختبار ============
if __name__ == "__main__":
    print("=" * 50)
    print("اختبار المحاكاة الحركية")
    print("=" * 50)
    
    # إنشاء المحاكي
    sim = KinematicSimulator()
    
    # إعداد سلسلة تروس
    print("\n1. إعداد سلسلة تروس:")
    gears = [
        {"id": "gear_driver", "teeth": 20},
        {"id": "gear_driven", "teeth": 40},
        {"id": "gear_output", "teeth": 30}
    ]
    sim.setup_gear_train(gears)
    print(f"   التروس: {len(gears)}")
    
    # عرض نسب التروس
    print("\n2. نسب التروس:")
    ratios = sim.get_gear_ratios()
    for r in ratios:
        print(f"   {r['gear1']} -> {r['gear2']}: {r['ratio']:.2f}")
    
    # محاكاة الدوران
    print("\n3. محاكاة الدوران:")
    result = sim.simulate_rotation("gear_driver", rpm=100, duration=1.0)
    print(f"   سرعة الإدخال: {result['input_rpm']} RPM")
    print(f"   السرعات الناتجة:")
    for gear_id, speed in result['output_speeds'].items():
        print(f"     {gear_id}: {speed:.2f} RPM")
    
    # اختبار GearMesh
    print("\n4. اختبار تعشيق التروس:")
    mesh = GearMesh()
    mesh.add_pair("g1", 20, "g2", 40)
    angles = mesh.rotate_gear("g1", math.pi)  # نصف دورة
    print(f"   g1: {math.degrees(angles['g1']):.1f}°")
    print(f"   g2: {math.degrees(angles['g2']):.1f}°")
    
    print("\n✅ اكتمل الاختبار بنجاح!")

"""
تكامل الصوت مع الذكاء | Voice-AI Integration
==============================================

يربط واجهة الصوت مع AI Bridge للحصول على تجربة
"كلمة → نموذج 3D" متكاملة.

المكونات:
- VoiceToShape: تحويل الأوامر الصوتية لنماذج
- VoiceTezniti: واجهة تزنيتي الصوتية الموحدة

المطور: باسل يحيى عبدالله
"""

import sys
import os
from typing import Dict, Any, Optional, List, Callable
from dataclasses import dataclass

# Add paths
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)
sys.path.insert(0, os.path.dirname(current_dir))

# Import components
from voice_interface import VoiceInterface, VoiceCommand, CommandType
from ai_bridge import TeznitiIntelligenceBridge, ShapeEquation


@dataclass
class VoiceShapeResult:
    """نتيجة تحويل الصوت لشكل"""
    success: bool
    voice_text: str
    command_type: str
    shape_equation: Optional[ShapeEquation]
    error: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "voice_text": self.voice_text,
            "command_type": self.command_type,
            "shape": {
                "type": self.shape_equation.equation_type if self.shape_equation else None,
                "parameters": self.shape_equation.parameters if self.shape_equation else {},
                "confidence": self.shape_equation.confidence if self.shape_equation else 0,
                "reasoning": self.shape_equation.reasoning if self.shape_equation else ""
            } if self.shape_equation else None,
            "error": self.error
        }


class VoiceToShape:
    """
    تحويل الأوامر الصوتية للأشكال 3D
    
    يجمع بين VoiceInterface و TeznitiIntelligenceBridge.
    """
    
    def __init__(self, vosk_model_path: str = None):
        print("🎙️ تهيئة نظام الصوت للأشكال...")
        
        # تهيئة واجهة الصوت
        self.voice = VoiceInterface(vosk_model_path)
        
        # تهيئة جسر الذكاء
        self.ai_bridge = TeznitiIntelligenceBridge()
        
        # سجل العمليات
        self.history: List[VoiceShapeResult] = []
        
        print("✅ تم تهيئة النظام بنجاح!")
    
    def listen_and_create(self, duration: float = 5.0) -> VoiceShapeResult:
        """
        استمع وأنشئ نموذج
        
        الخطوات:
        1. الاستماع للصوت
        2. تحويله لنص
        3. تحليله بواسطة Bayan
        4. إنتاج معادلة الشكل
        """
        # 1. الاستماع
        text = self.voice.recognizer.recognize_from_microphone(duration)
        
        if not text:
            return VoiceShapeResult(
                success=False,
                voice_text="",
                command_type="none",
                shape_equation=None,
                error="لم يتم التعرف على كلام"
            )
        
        # 2. تحويل للشكل
        return self.text_to_shape(text)
    
    def text_to_shape(self, text: str) -> VoiceShapeResult:
        """
        تحويل نص لشكل
        
        Args:
            text: النص الوارد (من الصوت أو مباشرة)
            
        Returns:
            نتيجة التحويل
        """
        try:
            # 1. تحليل الأمر
            voice_result = self.voice.process_text(text)
            command = voice_result["command"]
            
            # 2. إذا كان أمر إنشاء، استخدم AI Bridge
            if command["type"] == "create":
                shape_equation = self.ai_bridge.understand_request(text)
                
                result = VoiceShapeResult(
                    success=True,
                    voice_text=text,
                    command_type=command["type"],
                    shape_equation=shape_equation
                )
            else:
                # أوامر أخرى
                result = VoiceShapeResult(
                    success=True,
                    voice_text=text,
                    command_type=command["type"],
                    shape_equation=None
                )
            
            self.history.append(result)
            return result
            
        except Exception as e:
            return VoiceShapeResult(
                success=False,
                voice_text=text,
                command_type="error",
                shape_equation=None,
                error=str(e)
            )
    
    def get_shape_from_voice(self) -> Optional[ShapeEquation]:
        """
        واجهة بسيطة: استمع وأرجع الشكل
        """
        result = self.listen_and_create()
        return result.shape_equation if result.success else None
    
    def is_voice_available(self) -> bool:
        """هل التعرف على الصوت متاح؟"""
        return self.voice.recognizer.is_available
    
    def get_history(self) -> List[Dict[str, Any]]:
        """سجل العمليات"""
        return [r.to_dict() for r in self.history]


class VoiceTezniti:
    """
    واجهة تزنيتي الصوتية الموحدة
    
    تجمع كل القدرات في واجهة واحدة سهلة الاستخدام.
    """
    
    def __init__(self, vosk_model_path: str = None):
        self.converter = VoiceToShape(vosk_model_path)
        self.on_shape_created: Optional[Callable[[ShapeEquation], None]] = None
    
    def start_voice_mode(self):
        """
        بدء الوضع الصوتي التفاعلي
        
        يستمع للأوامر ويعالجها بشكل متكرر.
        """
        print("\n" + "=" * 50)
        print("🎙️ الوضع الصوتي لتزنيتي 3D")
        print("=" * 50)
        print("📢 قل أمرك... (للخروج قل 'خروج' أو اضغط Ctrl+C)")
        print()
        
        while True:
            try:
                result = self.converter.listen_and_create(duration=5.0)
                
                if result.voice_text.lower() in ["خروج", "exit", "quit"]:
                    print("👋 مع السلامة!")
                    break
                
                if result.success and result.shape_equation:
                    self._display_shape(result.shape_equation)
                    
                    if self.on_shape_created:
                        self.on_shape_created(result.shape_equation)
                else:
                    print(f"⚠️ {result.error or 'لم أفهم'}")
                
                print("-" * 30)
                
            except KeyboardInterrupt:
                print("\n👋 تم إيقاف الوضع الصوتي")
                break
    
    def _display_shape(self, shape: ShapeEquation):
        """عرض الشكل"""
        print(f"\n✅ تم إنشاء: {shape.equation_type}")
        print(f"📐 المعاملات:")
        for k, v in shape.parameters.items():
            print(f"   - {k}: {v}")
        print(f"🎯 الثقة: {shape.confidence:.2f}")
        print(f"💡 السبب: {shape.reasoning}")
    
    def quick_create(self, voice_command: str) -> Optional[ShapeEquation]:
        """
        إنشاء سريع من أمر نصي
        
        مثال: quick_create("ترس حلزوني قطر 50")
        """
        result = self.converter.text_to_shape(voice_command)
        return result.shape_equation if result.success else None
    
    def demo(self):
        """
        عرض توضيحي للنظام
        """
        print("\n" + "=" * 50)
        print("🎬 عرض توضيحي: الصوت إلى 3D")
        print("=" * 50)
        
        demo_commands = [
            "أنشئ ترس حلزوني قطر 50 موديول 2",
            "صمم رومان بلي قطر 52",
            "اعمل صندوق طول 100 عرض 80 ارتفاع 50",
            "أنشئ عمود طول 150 قطر 25"
        ]
        
        for cmd in demo_commands:
            print(f"\n🎤 الأمر: \"{cmd}\"")
            print("-" * 40)
            
            result = self.converter.text_to_shape(cmd)
            
            if result.success and result.shape_equation:
                self._display_shape(result.shape_equation)
            else:
                print(f"❌ فشل: {result.error}")
            
            print()
        
        print("=" * 50)
        print("✅ انتهى العرض التوضيحي")


# ============ اختبار ============
if __name__ == "__main__":
    print("=" * 60)
    print("🧪 اختبار تكامل الصوت مع الذكاء")
    print("=" * 60)
    
    # إنشاء الواجهة
    tezniti = VoiceTezniti()
    
    # التحقق من حالة الصوت
    print(f"\n📢 حالة Vosk: {'متاح ✅' if tezniti.converter.is_voice_available() else 'محاكاة ⚠️'}")
    
    # تشغيل العرض التوضيحي
    tezniti.demo()
    
    print("\n✅ اكتمل الاختبار!")

"""
واجهة الصوت - Voice Interface
==============================

تحويل الأوامر الصوتية العربية لنماذج 3D.

المكونات:
- VoiceRecognizer: التعرف على الصوت
- ArabicCommandParser: تحليل الأوامر
- VoiceInterface: الواجهة الموحدة

المطور: باسل يحيى عبدالله

ملاحظة: يتطلب تثبيت Vosk للتعرف الفعلي على الصوت:
pip install vosk sounddevice
"""

import sys
import os
from typing import List, Dict, Any, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import re
import json

# Add path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


class CommandType(Enum):
    """أنواع الأوامر الصوتية"""
    CREATE = "create"           # إنشاء قطعة
    MODIFY = "modify"           # تعديل قطعة
    DELETE = "delete"           # حذف قطعة
    EXPORT = "export"           # تصدير
    UNDO = "undo"               # تراجع
    HELP = "help"               # مساعدة
    QUERY = "query"             # استعلام
    UNKNOWN = "unknown"


@dataclass
class VoiceCommand:
    """أمر صوتي محلل"""
    text: str
    command_type: CommandType
    part_type: Optional[str]
    parameters: Dict[str, Any]
    confidence: float
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "type": self.command_type.value,
            "part_type": self.part_type,
            "parameters": self.parameters,
            "confidence": self.confidence
        }


class ArabicCommandParser:
    """
    محلل الأوامر العربية
    """
    
    def __init__(self):
        # كلمات الأوامر
        self.command_keywords = {
            CommandType.CREATE: [
                "أنشئ", "صمم", "اعمل", "ارسم", "كوّن", "اصنع",
                "create", "make", "design", "draw"
            ],
            CommandType.MODIFY: [
                "عدّل", "غيّر", "كبّر", "صغّر", "حرّك",
                "modify", "change", "resize", "move"
            ],
            CommandType.DELETE: [
                "احذف", "أزل", "امسح",
                "delete", "remove", "erase"
            ],
            CommandType.EXPORT: [
                "صدّر", "احفظ", "أرسل",
                "export", "save", "send"
            ],
            CommandType.UNDO: [
                "تراجع", "ألغِ",
                "undo", "cancel"
            ],
            CommandType.HELP: [
                "ساعدني", "مساعدة", "كيف",
                "help", "how"
            ]
        }
        
        # أنواع القطع
        self.part_keywords = {
            "helical_gear": ["ترس", "ترس حلزوني", "gear", "helical gear"],
            "spur_gear": ["ترس مستقيم", "spur gear"],
            "bearing": ["رومان", "رومان بلي", "bearing"],
            "bolt": ["برغي", "مسمار", "bolt", "screw"],
            "nut": ["صامولة", "nut"],
            "shaft": ["عمود", "محور", "shaft", "axis"],
            "box": ["صندوق", "علبة", "box", "container"],
            "plate": ["صفيحة", "لوح", "plate", "sheet"],
            "pipe": ["أنبوب", "ماسورة", "pipe", "tube"],
            "flange": ["فلنجة", "شفة", "flange"],
            "bracket": ["كتيفة", "حامل", "bracket", "mount"],
            "housing": ["غلاف", "صندوق", "housing", "enclosure"]
        }
        
        # أنماط استخراج الأرقام
        self.number_patterns = {
            "diameter": [
                r"قطر\s*(\d+(?:\.\d+)?)",
                r"diameter\s*(\d+(?:\.\d+)?)",
                r"(\d+(?:\.\d+)?)\s*مم قطر",
                r"قطره?\s*(\d+(?:\.\d+)?)"
            ],
            "teeth": [
                r"(\d+)\s*سن",
                r"(\d+)\s*teeth",
                r"أسنان\s*(\d+)"
            ],
            "length": [
                r"طول\s*(\d+(?:\.\d+)?)",
                r"length\s*(\d+(?:\.\d+)?)",
                r"(\d+(?:\.\d+)?)\s*مم طول"
            ],
            "width": [
                r"عرض\s*(\d+(?:\.\d+)?)",
                r"width\s*(\d+(?:\.\d+)?)"
            ],
            "height": [
                r"ارتفاع\s*(\d+(?:\.\d+)?)",
                r"height\s*(\d+(?:\.\d+)?)"
            ],
            "module": [
                r"موديول\s*(\d+(?:\.\d+)?)",
                r"module\s*(\d+(?:\.\d+)?)"
            ]
        }
    
    def parse(self, text: str) -> VoiceCommand:
        """
        تحليل نص الأمر
        """
        text_lower = text.lower()
        
        # 1. تحديد نوع الأمر
        command_type = self._detect_command_type(text_lower)
        
        # 2. تحديد نوع القطعة
        part_type = self._detect_part_type(text_lower)
        
        # 3. استخراج المعاملات
        parameters = self._extract_parameters(text)
        
        # 4. حساب الثقة
        confidence = self._calculate_confidence(command_type, part_type, parameters)
        
        return VoiceCommand(
            text=text,
            command_type=command_type,
            part_type=part_type,
            parameters=parameters,
            confidence=confidence
        )
    
    def _detect_command_type(self, text: str) -> CommandType:
        """اكتشاف نوع الأمر"""
        for cmd_type, keywords in self.command_keywords.items():
            if any(kw in text for kw in keywords):
                return cmd_type
        return CommandType.UNKNOWN
    
    def _detect_part_type(self, text: str) -> Optional[str]:
        """اكتشاف نوع القطعة"""
        for part_type, keywords in self.part_keywords.items():
            if any(kw in text for kw in keywords):
                return part_type
        return None
    
    def _extract_parameters(self, text: str) -> Dict[str, Any]:
        """استخراج المعاملات"""
        params = {}
        
        for param_name, patterns in self.number_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    try:
                        value = float(match.group(1))
                        params[param_name] = value
                        break
                    except:
                        pass
        
        # استخراج أرقام عامة
        if not params:
            numbers = re.findall(r"(\d+(?:\.\d+)?)", text)
            if numbers:
                params["value"] = float(numbers[0])
        
        return params
    
    def _calculate_confidence(self, cmd_type: CommandType, 
                              part_type: Optional[str],
                              params: Dict[str, Any]) -> float:
        """حساب الثقة"""
        confidence = 0.3
        
        if cmd_type != CommandType.UNKNOWN:
            confidence += 0.3
        
        if part_type:
            confidence += 0.2
        
        if params:
            confidence += 0.2
        
        return min(1.0, confidence)


class VoiceRecognizer:
    """
    التعرف على الصوت
    
    يستخدم Vosk للتعرف على الصوت العربي.
    """
    
    def __init__(self, model_path: str = None):
        self.model = None
        self.recognizer = None
        self.is_available = False
        self.sample_rate = 16000
        
        # Default model paths to search
        default_paths = [
            model_path,
            os.path.join(os.path.dirname(__file__), '../models/vosk-model-ar'),
            os.path.join(os.path.dirname(__file__), '../models/vosk-model-small-ar'),
            os.path.expanduser('~/.vosk/vosk-model-ar'),
            os.path.expanduser('~/.vosk/vosk-model-small-ar-0.22'),
            '/opt/vosk/model-ar',
        ]
        
        # محاولة تحميل Vosk
        try:
            from vosk import Model, KaldiRecognizer, SetLogLevel
            import sounddevice as sd
            
            # Reduce Vosk logging
            SetLogLevel(-1)
            
            # Try to find a valid model
            found_path = None
            for path in default_paths:
                if path and os.path.exists(path):
                    found_path = path
                    break
            
            if found_path:
                print(f"🎤 Loading Vosk model from: {found_path}")
                self.model = Model(found_path)
                self.recognizer = KaldiRecognizer(self.model, self.sample_rate)
                self.is_available = True
                print("✅ Vosk model loaded successfully")
            else:
                print("⚠️ Vosk model not found. Download Arabic model:")
                print("   wget https://alphacephei.com/vosk/models/vosk-model-small-ar-0.22.zip")
                print("   unzip vosk-model-small-ar-0.22.zip -d models/")
                print("   Using mock mode for now.")
        except ImportError:
            print("⚠️ Vosk not installed, using mock mode")
            print("   Install with: pip install vosk sounddevice")
    
    def recognize_from_microphone(self, duration: float = 5.0) -> Optional[str]:
        """
        التعرف من الميكروفون
        
        Args:
            duration: مدة التسجيل بالثواني
            
        Returns:
            النص المكتشف
        """
        if not self.is_available:
            return self._mock_recognition()
        
        try:
            import sounddevice as sd
            import numpy as np
            
            print(f"🎤 تحدث الآن... ({duration} ثواني)")
            
            # تسجيل الصوت
            audio = sd.rec(int(duration * self.sample_rate), 
                          samplerate=self.sample_rate, 
                          channels=1, dtype=np.int16)
            sd.wait()
            
            print("🔍 جاري التحليل...")
            
            # Reset recognizer
            self.recognizer.Reset()
            
            # Process in chunks
            chunk_size = 4000
            audio_bytes = audio.tobytes()
            
            for i in range(0, len(audio_bytes), chunk_size):
                chunk = audio_bytes[i:i + chunk_size]
                self.recognizer.AcceptWaveform(chunk)
            
            # Get final result
            result = json.loads(self.recognizer.FinalResult())
            text = result.get("text", "").strip()
            
            if text:
                print(f"✅ تم التعرف: {text}")
                return text
            else:
                print("⚠️ لم يتم التعرف على كلام")
                return None
            
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def recognize_from_file(self, audio_path: str) -> Optional[str]:
        """التعرف من ملف صوتي"""
        if not self.is_available:
            return self._mock_recognition()
        
        try:
            import wave
            
            with wave.open(audio_path, "rb") as wf:
                while True:
                    data = wf.readframes(4000)
                    if len(data) == 0:
                        break
                    self.recognizer.AcceptWaveform(data)
                
                result = json.loads(self.recognizer.FinalResult())
                return result.get("text", "")
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def _mock_recognition(self) -> str:
        """محاكاة التعرف"""
        # نماذج من الأوامر للاختبار
        samples = [
            "أنشئ ترس حلزوني قطر أربعين",
            "صمم صندوق طول مئة عرض خمسين",
            "اعمل رومان بلي قطر خمسة وعشرين"
        ]
        import random
        return random.choice(samples)


class VoiceInterface:
    """
    واجهة الصوت الموحدة
    
    تجمع التعرف والتحليل والتنفيذ.
    """
    
    def __init__(self, model_path: str = None):
        self.recognizer = VoiceRecognizer(model_path)
        self.parser = ArabicCommandParser()
        self.command_handlers: Dict[CommandType, Callable] = {}
        self.history: List[VoiceCommand] = []
    
    def register_handler(self, command_type: CommandType, handler: Callable):
        """تسجيل معالج أمر"""
        self.command_handlers[command_type] = handler
    
    def listen_and_execute(self, duration: float = 5.0) -> Optional[Dict[str, Any]]:
        """
        الاستماع وتنفيذ الأمر
        """
        # 1. التعرف
        text = self.recognizer.recognize_from_microphone(duration)
        
        if not text:
            return {"error": "لم أفهم ما قلته", "success": False}
        
        # 2. التحليل
        command = self.parser.parse(text)
        self.history.append(command)
        
        # 3. التنفيذ
        return self._execute_command(command)
    
    def process_text(self, text: str) -> Dict[str, Any]:
        """
        معالجة نص مباشرة (بدون صوت)
        """
        command = self.parser.parse(text)
        self.history.append(command)
        return self._execute_command(command)
    
    def _execute_command(self, command: VoiceCommand) -> Dict[str, Any]:
        """تنفيذ أمر"""
        result = {
            "command": command.to_dict(),
            "success": False,
            "message": ""
        }
        
        if command.command_type == CommandType.UNKNOWN:
            result["message"] = "لم أفهم الأمر"
            return result
        
        if command.confidence < 0.4:
            result["message"] = "الأمر غير واضح، هل يمكنك الإعادة؟"
            return result
        
        # تنفيذ المعالج المسجل
        handler = self.command_handlers.get(command.command_type)
        if handler:
            try:
                handler_result = handler(command)
                result["success"] = True
                result["message"] = "تم تنفيذ الأمر"
                result["handler_result"] = handler_result
            except Exception as e:
                result["message"] = f"خطأ في التنفيذ: {str(e)}"
        else:
            # استجابة افتراضية
            result["success"] = True
            result["message"] = self._generate_response(command)
        
        return result
    
    def _generate_response(self, command: VoiceCommand) -> str:
        """توليد استجابة"""
        if command.command_type == CommandType.CREATE:
            part = command.part_type or "قطعة"
            params = command.parameters
            
            msg = f"سأنشئ {part}"
            if params:
                param_str = ", ".join([f"{k}: {v}" for k, v in params.items()])
                msg += f" بالمواصفات: {param_str}"
            return msg
        
        elif command.command_type == CommandType.HELP:
            return """الأوامر المتاحة:
- أنشئ [نوع] [مواصفات]: لإنشاء قطعة
- عدّل [خاصية]: لتعديل القطعة
- احذف: لحذف القطعة المحددة
- صدّر: لتصدير النموذج"""
        
        return "تم استلام الأمر"
    
    def get_available_commands(self) -> List[str]:
        """الأوامر المتاحة"""
        return [
            "أنشئ ترس قطر 40",
            "صمم صندوق طول 100 عرض 50 ارتفاع 30",
            "اعمل رومان بلي قطر 52",
            "أنشئ عمود طول 150 قطر 25",
            "صمم برغي M10 طول 50"
        ]
    
    def get_history(self) -> List[Dict[str, Any]]:
        """سجل الأوامر"""
        return [cmd.to_dict() for cmd in self.history]


# ============ اختبار ============
if __name__ == "__main__":
    print("=" * 50)
    print("اختبار واجهة الصوت")
    print("=" * 50)
    
    interface = VoiceInterface()
    
    # اختبار التحليل
    print("\n1. اختبار تحليل الأوامر:")
    
    commands = [
        "أنشئ ترس حلزوني قطر 40 وموديول 2",
        "صمم صندوق طول 100 عرض 50",
        "احذف القطعة المحددة",
        "ساعدني"
    ]
    
    for cmd_text in commands:
        result = interface.process_text(cmd_text)
        print(f"\n   الأمر: {cmd_text}")
        print(f"   النوع: {result['command']['type']}")
        print(f"   القطعة: {result['command']['part_type']}")
        print(f"   المعاملات: {result['command']['parameters']}")
        print(f"   الاستجابة: {result['message']}")
    
    # عرض الأوامر المتاحة
    print("\n2. الأوامر المتاحة:")
    for cmd in interface.get_available_commands()[:3]:
        print(f"   - {cmd}")
    
    print("\n✅ اكتمل الاختبار بنجاح!")

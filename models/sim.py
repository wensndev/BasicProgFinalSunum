import json
import os
import random
from datetime import datetime, timedelta

class Sim:
    def __init__(self, name, gender, age=25):
        self.name = name
        self.gender = gender
        self.age = age
        self.mood = 50  # 0-100 arası
        self.energy = 100  # 0-100 arası
        self.hunger = 0  # 0-100 arası (0: tok, 100: aç)
        self.hygiene = 100  # 0-100 arası
        self.social = 50  # 0-100 arası
        self.money = 1000
        self.job = None
        self.relationships = {}
        self.current_date = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
        self.state = "normal"  # normal, depressed, flirty, etc.
    
    def update_needs(self, **kwargs):
        """Sim'in ihtiyaçlarını günceller."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                current_value = getattr(self, key)
                new_value = max(0, min(100, current_value + value))
                setattr(self, key, new_value)
    
    def get_status(self):
        """Sim'in durumunu döndürür."""
        return {
            "name": self.name,
            "gender": self.gender,
            "age": self.age,
            "mood": self.mood,
            "energy": self.energy,
            "hunger": self.hunger,
            "hygiene": self.hygiene,
            "social": self.social,
            "money": self.money,
            "job": self.job,
            "state": self.state,
            "date": self.current_date.strftime("%d.%m.%Y %H:%M")
        }
    
    def advance_time(self, hours=1):
        """Zamanı ilerletir."""
        self.current_date += timedelta(hours=hours)
        
        # Zamanla ihtiyaçlar değişir
        self.update_needs(
            energy=-5 * hours,
            hunger=5 * hours,
            hygiene=-3 * hours,
            social=-2 * hours
        )
        
        # Mood hesaplaması
        self.calculate_mood()
    
    def calculate_mood(self):
        """Mood'u diğer faktörlere göre hesaplar."""
        factors = {
            "energy": lambda x: (x - 50) * 0.2,
            "hunger": lambda x: (100 - x - 50) * 0.2,
            "hygiene": lambda x: (x - 50) * 0.1,
            "social": lambda x: (x - 50) * 0.15
        }
        
        mood_change = sum(map(lambda factor: factors[factor](getattr(self, factor)), factors))
        self.mood = max(0, min(100, self.mood + mood_change))
        
        # Durum kontrolü
        if self.mood < 20:
            self.state = "depressed"
        elif self.energy < 20:
            self.state = "exhausted"
        elif self.hunger > 80:
            self.state = "starving"
        elif self.social > 80:
            self.state = "flirty"
        else:
            self.state = "normal"
    
    def save(self):
        """Sim verilerini kaydeder."""
        data = {
            "name": self.name,
            "gender": self.gender,
            "age": self.age,
            "mood": self.mood,
            "energy": self.energy,
            "hunger": self.hunger,
            "hygiene": self.hygiene,
            "social": self.social,
            "money": self.money,
            "job": self.job,
            "state": self.state,
            "current_date": self.current_date.isoformat(),
            "relationships": self.relationships
        }
        
        try:
            with open(f"save_{self.name}.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Kayıt hatası: {e}")
            return False
    
    @classmethod
    def load(cls, name):
        """Kaydedilmiş Sim verilerini yükler."""
        try:
            with open(f"save_{name}.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            
            sim = cls(data["name"], data["gender"], data["age"])
            sim.mood = data["mood"]
            sim.energy = data["energy"]
            sim.hunger = data["hunger"]
            sim.hygiene = data["hygiene"]
            sim.social = data["social"]
            sim.money = data["money"]
            sim.job = data["job"]
            sim.state = data["state"]
            sim.current_date = datetime.fromisoformat(data["current_date"])
            sim.relationships = data["relationships"]
            
            return sim
        except FileNotFoundError:
            return None
        except Exception as e:
            print(f"Yükleme hatası: {e}")
            return None 
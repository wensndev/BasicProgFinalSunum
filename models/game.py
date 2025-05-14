import os
import sys
import time
import random
import inquirer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress
from rich.table import Table

from models.sim import Sim

class Game:
    def __init__(self, console=None):
        self.console = console or Console()
        self.sim = None
        self.event_generator = None
        self.day_counter = 1
        self.quit_game = False
    
    def clear_console(self):
        """Konsolu temizler"""
        self.console.clear()
    
    def start(self):
        """Oyunu başlatır."""
        self.clear_console()
        self.show_main_menu()
        
        while not self.quit_game:
            if self.sim:
                self.clear_console()
                self.show_status()
                self.show_actions()
            else:
                break
    
    def show_main_menu(self):
        """Ana menüyü gösterir."""
        self.clear_console()
        choices = [
            "Yeni Oyun",
            "Kayıtlı Oyun Yükle",
            "Çıkış"
        ]
        
        questions = [
            inquirer.List('choice',
                          message="Sim Hayatı'na Hoş Geldiniz!",
                          choices=choices),
        ]
        
        answer = inquirer.prompt(questions)
        
        if answer['choice'] == "Yeni Oyun":
            self.clear_console()
            self.create_new_sim()
        elif answer['choice'] == "Kayıtlı Oyun Yükle":
            self.clear_console()
            self.load_saved_game()
        else:
            self.quit_game = True
            sys.exit(0)
    
    def create_new_sim(self):
        """Yeni bir Sim oluşturur."""
        questions = [
            inquirer.Text('name', message="Karakterinizin adı nedir?"),
            inquirer.List('gender',
                          message="Karakterinizin cinsiyeti nedir?",
                          choices=["Erkek", "Kadın", "Diğer"]),
            inquirer.Text('age', message="Karakterinizin yaşı nedir? (18-80)", validate=lambda _, x: x.isdigit() and 18 <= int(x) <= 80)
        ]
        
        answers = inquirer.prompt(questions)
        
        self.sim = Sim(answers['name'], answers['gender'], int(answers['age']))
        self.console.print(f"[green]Tebrikler! {self.sim.name} oluşturuldu.[/green]")
        
        # İş seçimi
        job_questions = [
            inquirer.List('job',
                          message="Karakterinizin mesleği nedir?",
                          choices=["Yazılımcı", "Öğretmen", "Doktor", "Sanatçı", "İşsiz"]),
        ]
        
        job_answer = inquirer.prompt(job_questions)
        self.sim.job = job_answer['job']
        
        time.sleep(1)
        self.clear_console()

    def save_game(self):
        """Oyunu kaydeder."""
        if self.sim.save():
            self.console.print(f"[green]Oyun başarıyla kaydedildi: save_{self.sim.name}.json[/green]")
        else:
            self.console.print("[red]Oyun kaydedilirken bir hata oluştu![/red]")
        
        time.sleep(2)
        self.clear_console()

    def load_saved_game(self):
        """Kaydedilmiş oyunu yükler."""
        # Kayıtlı oyunları bul
        saved_games = []
        for file in os.listdir("."):
            if file.startswith("save_") and file.endswith(".json"):
                saved_games.append(file[5:-5])  # "save_" ve ".json" kısmını çıkar
        
        if not saved_games:
            self.console.print("[red]Kayıtlı oyun bulunamadı![/red]")
            time.sleep(2)
            self.clear_console()
            self.show_main_menu()
            return
        
        saved_games.append("Ana Menüye Dön")
        
        questions = [
            inquirer.List('save',
                          message="Hangi kayıtlı oyunu yüklemek istersiniz?",
                          choices=saved_games),
        ]
        
        answer = inquirer.prompt(questions)
        
        if answer['save'] == "Ana Menüye Dön":
            self.clear_console()
            self.show_main_menu()
            return
        
        self.sim = Sim.load(answer['save'])
        if self.sim:
            self.console.print(f"[green]{self.sim.name} başarıyla yüklendi![/green]")
            time.sleep(1)
            self.clear_console()
        else:
            self.console.print("[red]Oyun yüklenirken bir hata oluştu![/red]")
            time.sleep(2)
            self.clear_console()
            self.show_main_menu()
    
    def show_status(self):
        """Sim'in durumunu gösterir."""
        status = self.sim.get_status()
        
        self.console.print("\n")
        self.console.print(Panel(f"[bold]{status['name']} - Gün {self.day_counter}[/bold] - {status['date']}", border_style="green"))
        
        table = Table(show_header=False, box=None)
        table.add_column("Özellik", style="cyan")
        table.add_column("Değer", style="yellow")
        
        table.add_row("Durum", status['state'])
        table.add_row("Ruh Hali", f"{status['mood']}/100")
        table.add_row("Enerji", f"{status['energy']}/100")
        table.add_row("Açlık", f"{status['hunger']}/100")
        table.add_row("Temizlik", f"{status['hygiene']}/100")
        table.add_row("Sosyallik", f"{status['social']}/100")
        table.add_row("Para", f"{status['money']}₺")
        table.add_row("Meslek", status['job'] or "İşsiz")
        
        self.console.print(table)
        self.console.print("\n")
    
    def show_actions(self):
        """Kullanılabilir aksiyonları gösterir."""
        actions = [
            "Ye",
            "Çalış",
            "Uyu",
            "Banyo Yap",
            "Sosyalleş ve İlişkiler",
            "Oyunu Kaydet",
            "Ana Menüye Dön"
        ]
        
        questions = [
            inquirer.List('action',
                          message="Ne yapmak istersiniz?",
                          choices=actions),
        ]
        
        answer = inquirer.prompt(questions)
        
        if answer['action'] == "Oyunu Kaydet":
            self.clear_console()
            self.save_game()
        elif answer['action'] == "Ana Menüye Dön":
            self.clear_console()
            self.show_main_menu()
        else:
            self.clear_console()
            self.console.print(f"[red]Eklenecek.[/red]")
            self.console.print(f"[green]3 saniye içinde ana menüye dönülüyor...[/green]\n")
            with Progress() as progress:
                task = progress.add_task("", total=100)
                while not progress.finished:
                    progress.update(task, advance=1.6667)  # Her adımda %1.6667 ilerle
                    time.sleep(0.05)  # 0.05 saniyede bir güncelle
            self.clear_console()
            self.show_status()
            self.show_actions()
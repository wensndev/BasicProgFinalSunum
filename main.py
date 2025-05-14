import sys
import time
import pyfiglet
from rich.console import Console
from rich.panel import Panel


from models.game import Game

def main():
    console = Console()
    
    # Konsolu temizle
    console.clear()
    
    # EA intro
    ea_text = pyfiglet.figlet_format("EA GAMES", font="slant")
    console.print(Panel(ea_text, border_style="bright_blue"))
    time.sleep(3)
    
    # Konsolu temizle
    console.clear()
    
    # Oyun başlığı
    title = pyfiglet.figlet_format("SIMS 1960", font="slant")
    console.print(Panel(title, border_style="bright_green"))
    time.sleep(2)
    
    # Oyunu başlat
    try:
        game = Game(console)
        game.start()
    except KeyboardInterrupt:
        console.print("\n[bold red]Oyundan çıkılıyor...[/bold red]")
        sys.exit(0)
    except Exception as e:
        console.print(f"[bold red]Hata oluştu: {e}[/bold red]")
        sys.exit(1)

if __name__ == "__main__":
    main() 
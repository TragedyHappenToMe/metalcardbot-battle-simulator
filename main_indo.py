import json
import random
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

class Character():
    def __init__(self, name, hp, attack, defense):
        self.name = name
        self.hp = hp
        self.attack = attack
        self.defense = defense
        
    def take_damage(self, damage):
        act_damage = damage - random.randint(0, self.defense)
        if self.hp < act_damage:
            self.hp = 0
        else:
             self.hp -= act_damage
        return act_damage

def load_characters():
    with open("characters.json", 'r') as file:
        data = json.load(file)
    
    characters = []    
    for item in data:
        characters.append(Character(item["name"], item["hp"], item["attack"], item["defense"]))

    return characters
    
def select_character(characters):
    
    table = Table(title="Daftar Metal Cardbot")
    
    table.add_column("No")
    table.add_column("Nama")
    table.add_column("HP")
    table.add_column("Attack")
    table.add_column("Defense")
    
    for no, char in enumerate(characters, start = 1):
        table.add_row(str(no), str(char.name), str(char.hp), str(char.attack), str(char.defense))
    
    console = Console()
    console.print(table)
    while True:
        try:
            pilih = int(input("Pilih nomor karakter yang ingin dipilih: "))
            karakter = characters[pilih-1]
            print(f"\nKarakter {karakter.name} berhasil dipilih")
            return karakter
        
        except IndexError:
            print("Karakter hanya mempunyai nomor 1 sampai 12!")
        except ValueError:
            print("Input harus berupa angka!")

def cpu_select(characters):
    karakter = random.choice(characters)
    
    print(f"Karakter yang dilawan adalah {karakter.name}")
    return karakter
    
def battle(player, cpu):
    print()
    print("="*15)
    print("Battle Dimulai!")
    print("="*15)
    
    player_max_hp = player.hp
    cpu_max_hp = cpu.hp
    console = Console()
    giliran = 0
    while True:
        # player
        giliran += 1
        print()
        console.print(Panel.fit(f"+ Giliran {giliran}", style="bold"))
        
        console.print(f"[magenta3]{player.name}[/magenta3] menyerang dengan damage [yellow]{cpu.take_damage(player.attack)}[/yellow]")
        print(f"HP {cpu.name} tersisa {cpu.hp}")
        console.print(hp_bar(cpu.hp, cpu_max_hp))
        if cpu.hp == 0:
            print(f"\n{player.name} telah mengalahkan {cpu.name}")
            break
        # cpu
        console.print(f"[magenta3]{cpu.name}[/magenta3] menyerang dengan damage [yellow]{player.take_damage(cpu.attack)}[/yellow]")
        print(f"HP {player.name} tersisa {player.hp}")
        console.print(hp_bar(player.hp, player_max_hp))
        if player.hp == 0:
            print(f"\n{cpu.name} telah mengalahkan {player.name}")
            break

def hp_bar(hp, max_hp, length=20):
    filled = int((hp / max_hp) * length)
    bar = "█" * filled + "░" * (length - filled)
    return f"[green]{bar}[/green] {hp}/{max_hp}"

def main():
    characters = load_characters()
    player = select_character(characters)
    sisa = [char for char in characters if char != player]
    cpu = cpu_select(sisa)
    battle(player, cpu)
    
if __name__ == "__main__":
    main()
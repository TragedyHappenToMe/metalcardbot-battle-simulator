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
    table = Table(title="Metal Cardbot Roster")
    
    table.add_column("No")
    table.add_column("Name")
    table.add_column("HP")
    table.add_column("Attack")
    table.add_column("Defense")
    
    for no, char in enumerate(characters, start=1):
        table.add_row(str(no), str(char.name), str(char.hp), str(char.attack), str(char.defense))
    
    console = Console()
    console.print(table)
    while True:
        try:
            pilih = int(input("Choose your character (1-12): "))
            karakter = characters[pilih-1]
            console.print(f"\nCharacter [cyan]{karakter.name}[/cyan] selected!")
            return karakter
        except IndexError:
            console.print("[red]Please choose a number between 1 and 12![/red]")
        except ValueError:
            console.print("[red]Input must be a number![/red]")

def cpu_select(characters):
    karakter = random.choice(characters)
    console = Console()
    console.print(f"Your opponent is [red]{karakter.name}[/red]!")
    return karakter
    
def battle(player, cpu):
    console = Console()
    console.print(Panel.fit("⚔ Battle Start! ⚔", style="bold red"))
    
    player_max_hp = player.hp
    cpu_max_hp = cpu.hp
    giliran = 0
    while True:
        giliran += 1
        console.print()
        console.print(Panel.fit(f"⚔ Round {giliran}", style="bold"))
        
        console.print(f"[cyan]{player.name}[/cyan] attacks for [yellow]{cpu.take_damage(player.attack)}[/yellow] damage!")
        console.print(f"HP {cpu.name}: {hp_bar(cpu.hp, cpu_max_hp)}")
        if cpu.hp == 0:
            console.print(f"\n[green]{player.name} defeated {cpu.name}! You win![/green]")
            break

        console.print(f"[magenta]{cpu.name}[/magenta] attacks for [yellow]{player.take_damage(cpu.attack)}[/yellow] damage!")
        console.print(f"HP {player.name}: {hp_bar(player.hp, player_max_hp)}")
        if player.hp == 0:
            console.print(f"\n[red]{cpu.name} defeated {player.name}! You lose![/red]")
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
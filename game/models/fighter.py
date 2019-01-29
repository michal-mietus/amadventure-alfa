class Fighter:
    def __init__(self, hero, enemy):
        self.health = hero.health
        self.physical_damage = self.calculate_physical_damage(hero, enemy)
        self.magical_damage = self.calculate_magical_damage(hero, enemy)

    def hit_enemy(self, enemy):
        enemy.health -= self.physical_damage + self.magical_damage

    def calculate_physical_damage(self, hero, enemy):
        physical_damage = hero.physical_attack / enemy.defense
        return physical_damage

    def calculate_magical_damage(self, hero, enemy):
        magical_damage = hero.magic_attack / enemy.magic_resist
        return magical_damage

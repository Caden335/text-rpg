rpg_races = (('Human', 0, 0, 0, 1),
             ('Elf', 0, 0, 2, -1),
             ('Dwarf', 0, 2, -1, 0),
             ('Orc', 0, -1, 0, 2))

class Race:
    """Contains race name and stat additions.

    Attributes:
        name (str): name
        atk
        ac
        dge
        max_hp
    """
    
    def __init__(self, name, atk, ac, dge, max_hp):
        self.name = name
        self.atk = atk
        self.ac = ac
        self.dge = dge
        self.max_hp = max_hp
        
    def __init__(self, list: data): #init overload for if you want to init using a tuple
        self.name = data[0]
        self.atk = data[1]
        self.ac = data[2]
        self.dge = data[3]
        self.max_hp = data[4]
    
    
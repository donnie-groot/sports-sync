###### standard library imports ######
from dataclasses import dataclass
from datetime import datetime

###### 3rd party imports ######
#import from thing i downloaded 

###### local imports ######



@dataclass
class Game:
    sport: str
    game_id: int
    start: datetime
    is_tbd: bool
    home: str
    away: str




if __name__ == "__main__":
    test = Game(sport='cbb', game_id=374601, start=datetime(2026, 11, 3, 19, 0), is_tbd=False, home="Kentucky", away="Louisville")
    
    print(test)
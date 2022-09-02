from .base import BaseInstance

class Hangman(BaseInstance):
   
    class data:
        word        = "COLGADO"
        keys        = []
        turn        = 0
        control     = False
        minPlayers  = 1
        maxPlayers  = 12

    async def screen(self, ctx):
        text = f"[c]  -- Sala: {self.roomId} --\n[c]  ----------------------  \n\n[c]"
        for key in self.data.word:
            if key in self.data.keys: text += f"{key} "
            else                    : text += "_ "

        text += "\n[c]\n[c]No: "
        for key in self.data.keys:
            if key not in self.data.word: text += f"{key} "
        
        text += f"\n\n[c]Turno de: {self.players[self.data.turn % len(self.players)][1]}"
        return text
    
    async def logic(self, ctx, key):
        key = key.upper()
        if len(key) > 1 and  key.upper() != self.data.word:
            return "Debe poner solo una letra"    
        elif key == self.data.word:
            for letter in self.data.word:
                if letter not in self.data.keys: self.data.keys.append(letter)
        if key in self.data.keys : return "La letra ya ha sido puesta, pruebe con otra"
        else:
            self.data.keys.append(key)
            self.data.turn += 1
        return await self.screen()

    async def win(self):
        for key in self.data.word:
            if key not in self.data.keys: return False
        return True
    
    async def lose(self):
        return

# Games

class Player():
    """# ? Учасник гри"""
    def __init__(self, name, score=0):
        self.name = name
        self.score = score
    
    def __str__(self):
        rep = self.name + ':\t' + str(self.score)
        return rep
    
def ask_yes_no(question):
    """Питання з відповіддю *Так* або *Ні*"""
    response = None
    while response not in ('y', 'n'):
        response = input(question.lower())
    return response

def ask_number(question, low, high):
    """Просить ввести число з заданого діапазону"""
    response = None
    while response not in range(low, high):
        response = int(input(question))
    return response

if __name__ == '__main__':
    print('Модуль запущений напряму, а не через імпорт.')
    input('\nНатисніть Enter, щоб вийти.')
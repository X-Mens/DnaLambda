from app.model.DnaType import DnaType

dx = [1, 2, 3]
dy = [1, 2, 3]


class Dna:

    def __init__(self, dna: list):
        self.adn = dna
        self.adnSize = len(dna)

    def is_mutant(self):

        is_mutant = False
        if self.adnSize > 3:
            count_sequence_same = 0
            for i in range(self.adnSize):
                for j in range(self.adnSize):
                    count_sequence_same += self.__verify_horizontal(i, j)
                    count_sequence_same += self.__verify_vertical(i, j)
                    count_sequence_same += self.__verify_oblique(i, j)
            is_mutant = count_sequence_same >= 2
        return is_mutant

    def __verify_oblique(self, x, y):
        character = self.adn[x][y]
        oblique_up = True
        oblique_down = True
        for i in range(1, 4, 1):
            oblique_up &= self.__is_there_sequence(y - i >= 0 and x + i < self.adnSize, x + i, y - i, character)
            oblique_down &= self.__is_there_sequence(y + i < self.adnSize and x + i < self.adnSize,
                                                     x + i, y + i, character)
        if oblique_up and oblique_down: return 2
        if oblique_up or oblique_down:
            return 1
        else:
            return 0

    def __is_there_sequence(self, condition, i, j, character):
        is_there_sequence = True
        if condition:
            character_to_compare = self.adn[i][j]
            if character_to_compare != character:
                is_there_sequence = False
        else:
            is_there_sequence = False
        return is_there_sequence

    def __verify_vertical(self, x, y):
        character = self.adn[x][y]
        for i in range(1, 4, 1):
            if y + i >= self.adnSize:
                return 0
            character_to_compare = self.adn[x][y + i]
            if character_to_compare != character:
                return 0
        return 1

    def __verify_horizontal(self, x, y):
        character = self.adn[x][y]
        for i in range(1, 4, 1):
            if x + i >= self.adnSize:
                return 0
            character_to_compare = self.adn[x + i][y]
            if character_to_compare != character:
                return 0
        return 1

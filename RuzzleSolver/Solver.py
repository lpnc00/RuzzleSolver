from MTrie import MTrie
from Languages import LANGUAGES, LETTER_SCORE


class Graph:
    def __init__(self, grid, bonus, lang):
        self.nodes = [(0, 0), (0, 1), (0, 2), (0, 3),
                      (1, 0), (1, 1), (1, 2), (1, 3),
                      (2, 0), (2, 1), (2, 2), (2, 3),
                      (3, 0), (3, 1), (3, 2), (3, 3)]

        self.chars = {id: c for id, c in zip
        (self.nodes, [item for sublist in grid for item in sublist])}

        self.mults = {id: b for id, b in zip
        (self.nodes, [item for sublist in bonus for item in sublist]) if b != ''}

        self.dict = MTrie(LANGUAGES[lang])
        self.scores = self.__gen_scores(lang)

        self.adj_l = self.__gen_adj_l()

    def __gen_scores(self, lang):
        scores = {id: LETTER_SCORE[lang][c] for id, c in self.chars.items()}
        multiplier = dict()
        tempw = {'DW': 2, 'TW': 3}
        templ = {'DL': 2, 'TL': 3}
        for k, v in self.mults.items():
            if v in tempw.keys():
                multiplier[k] = tempw[v]
            else:
                scores[k] *= templ[v]
        self.mults = multiplier
        return scores

    def __gen_adj_l(self):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)]
        adj_l = dict()
        for x, y in self.nodes:
            temp_lst = []
            for cx, cy in directions:
                if (0 <= x + cx < 4) and (0 <= y + cy < 4):
                    temp_lst.append((x + cx, y + cy))
            adj_l[(x, y)] = temp_lst
        return adj_l
    
    def word(self, coords):
        return ''.join([self.chars[(xy)] for xy in coords]).lower()

    def score(self, coords):
        score = 0
        mult = 1
        length_bonus = 0
        if len(coords) > 4:
            length_bonus += 5 * (len(coords) - 4)
        for xy in coords:
            if xy in self.mults.keys():
                mult *= self.mults[(xy)]
            score += self.scores[(xy)]

        return score * mult + length_bonus

    def summary(self):
        summary = {}
        for path in self.BFS():
            word = self.word(path)
            score = self.score(path)
            if word not in summary or summary[word][1] < score:
                summary[word] = (word, score, path)
        return summary

    def BFS(self):
        valid_words = []
        for s in self.nodes:
            queue = [[s]]
            while queue:
                current = queue.pop(0)
                current_word = self.word(current)
                if len(current_word) > 1 and current_word in self.dict:
                    valid_words.append(current)
                if self.dict.keys(current_word):
                    for node in self.adj_l[current[-1]]:
                        temp_path = current[:]
                        if node not in temp_path:
                            temp_path.append(node)
                            queue.append(temp_path)
        return valid_words

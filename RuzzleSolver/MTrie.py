from marisa_trie import Trie


class MTrie(Trie):
    def __init__(self, file_path):
        if file_path.endswith(".marisa"):
            super().__init__()
            self.load(file_path)
        else:
            super().__init__(self.__load_txt_file(file_path))

    @staticmethod
    def __load_txt_file(file_path):
        with open(file_path, "r") as f:
            words = []
            for line in f:
                words.append(line.strip())
        return words

# save .txt files to .marisa files
# MTrie('raw_languages/es_ES.txt').save('mt_languages/es.marisa')
# MTrie('raw_languages/en_GB.txt').save('mt_languages/en.marisa')
# MTrie('raw_languages/it_IT.txt').save('mt_languages/it.marisa')

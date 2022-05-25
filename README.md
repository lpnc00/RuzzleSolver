# RuzzleSolver

**RuzzleSolver** provides a GUI, which allow user to input a Ruzzle grid and it will list all the valid words with their scores.

* Date: 25-05-2022
* Developers: 
    * Luca Panchetti
    * Matteo Cassarino
    * Salvatore Messina
    * Roberto Peri
    * Beniamino Guida

## Usage

    $ python RuzzleSolver
	
Run the command in terminal in the current path.

You need the `marisa-trie` (`pip install marisa-trie`) and `Unidecode` (`pip install Unidecode`) Python packages to run RuzzleSolver.<br>
[MARISA Trie](https://pypi.org/project/marisa-trie/), [Unidecode](https://pypi.org/project/Unidecode/).

## Scoring Rules

1. Only words in the given dictionary are valid.
2. Only words at least two letters long are valid.
3. A path (i.e. a sequence of adjacent letters) cannot intersect itself, that is, each board cell can be used at most once per path.
4. Only one path per word counts, that is, only the first path forming a word will get points.
5. The score of a path is the sum of the scores of its letters (each multiplied by its letter multiplier, if any),
times the product of the word multipliers (if any).
6. An additional bonus length score is added if word is longer than 4. The word length points are 5 times word_length-4

## Available Languages

The following languages are supported, which means that the code includes
a dictionary, letter score and letter frequency for each of them:

* `Italian`
* `English`
* `Spanish`


## Dictionary Files

The dictionary files were compiled from the corresponding [Hunspell](http://hunspell.github.io/)
dictionaries found [here](https://cgit.freedesktop.org/libreoffice/dictionaries/tree/).
A plain text, UTF-8 encoded file, with one word per line was created using `hunspell-tools` package on Ubuntu-20.04 terminal
with Windows Subsystem for Linux.

    $ unmunch language.dic language.aff > language.txt

Using this command a plain text is obtained:

    a
    A
    AA
    AAA
    Aachen
    aah
    Aaliyah
    ...

The words will undergo diacritics removal, lowercase normalization
and deletion long words (length>16), resulting in a dictionary of lowercased ASCII words.
For example, the Italian word `città` (city) will become `citta`.<br>
All the raw files can be found in `RuzzleSolver/raw_languages`.

Then, dictionary files are compiled as MARISA files,
which are binary serializations of MARISA tries, to make the loading time shorter.
To compile a plain text dictionary into a MARISA binary dictionary, we load .txt file with the method `__load_txt_file` in `MTrie` class,
then we have saved in `.marisa` file by using `marisa_trie.Trie.save`.

The `MTrie.MTrie` class just load `.marisa` file from `RuzzleSolver/mt_languages` as a Trie and import all the funcion of `marisa_trie.Trie`

## GUI

The GUI is created using `tkinter` python package.

The class `GUI.App` has four methods:

* `__WM_destroy`, which destroys every window, used to pass from a level to another;
* `__Letter`, which allows the user to input letters in the grid and select language;
* `__Bonus`, which allows the user to input bonus in the grid;
* `__Solve`, which shows to the user the summary of `Solver.Graph`, i.e. a list of words sorted by descending score, where each word can be double clicked and a new window appear with the animation of the path on the grid.

The grid has dimensions `4x4`, user can input only letters, which are already normalized, symbols and numbers are not accept.<br>
The grid cannot contain holes, otherwise an error messagebox will appear.<br>
User must select a language, otherwise an error messagebox will appear.

## Solver Strategy

The program solves a given grid using a modified BFS.

First of all `Solver.Graph` class must be initialized, with a list of list containing letters, a list of lists containing bonuses and a string language.<br>
A graph will be created using coordinates as nodes (i.e. (0,0) will be the top left corner of the grid). Coordinates will henceforth be referred to as nodes
Through dictionaries with nodes as key, it will access letters, bonuses and scores. Scores are computed by accessing `Languages.LETTER_SCORE`,
a dictionary of dictionaries containing score for each letter for each language, letter multiplier will be computed during the generation and deleted from bonuses,
leaving only word multipliers. Then, it creates an adjacency list, a dictionary with nodes as keys and lists of adjacent nodes as values (i.e. `{(0,0):[(0,1),(1,0),(1,1)],...}`),
these are letters which are accessible from a given cell. Finally it creates a Trie object calling `MTrie.MTrie` with the corresponding `.marisa` file path depending on the language by accessing `Languages.LANGUAGES`.

`Solver.Graph` has four functions:

* `word`, which return the word formed, given a path;
* `score`, which return the the total score obtained, given a path (i.e. word score);
* `summary`, which return a dictionary with all the words obtainable as keys and tuples containing the word, the score and the path as values;
* `BFS`,  which return a list of lists of nodes (i.e. paths), which form valid words.

To find all the path, a modified-BFS exploration for each node is performed. <br>
The function differs from the classic BFS:
1. The queue contains list of paths and not just adjacent nodes of the dequeued value
(i.e. in the first step for the node `(0,0)`, the queue will be `[[(0,0),(0,1)],[(0,0),(1,0)],[(0,0),(1,1)]]`),
in this way it will keep track of all the path and will check adjacency list of the last node of the path.
2. After dequeuing a path, if it is longer than 1, it will check if the current word
is a valid word by consulting the Trie, and if so it will append the path in the temporary list which will be returned
(i.e. if the current word is `city`, the path will be appended).
3. Adjacency list will be consulted only if the current word is a prefix by consulting the Trie
(i.e. if the current word is `qz`, none words exists with this prefix, hence the BFS will move on).
4. If the adjacency list is consulted, only nodes which are not already in the current path will be added (i.e. path cannot self-intersect).






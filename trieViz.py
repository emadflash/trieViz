import sys
import argparse
from typing import List

import graphviz

class Trie:
    def __init__(self, isEOW: bool = False):
        self.isEOW: bool = isEOW
        self.childs: List['Trie'] = [None] * 256

    def insert(self, word: str) -> None:
        def mInsert(root: 'Trie', word: str) -> None:
            if len(word) == 0:
                return

            letterIdx: int = Trie.chrToChildIdx(word[0])

            if root.childs[letterIdx] is None:
                root.childs[letterIdx] = Trie(False)

            if len(word) == 1:
                root.childs[letterIdx].isEOW = True
            else:
                mInsert(root.childs[letterIdx], word[1:])

        return mInsert(self, word)

    def insertList(self, l: List[str]) -> None:
        for s in l:
            self.insert(s)

    def search(self, word: str) -> bool:
        pass
        
    def startsWith(self, prefix: str) -> bool:
        pass

    def chrToChildIdx(ch) -> int:
        return ord(ch)

    def childIdxToAscii(idx) -> str:
        return chr(idx)

    def getDigraph(self, filename: str = 'trieViz.gv'):
        digraph = graphviz.Digraph("trie", filename = filename)
        iterIdx: int = 0

        def dumpTrie(parentIterIdx: int, childs: List['Trie']):
            nonlocal iterIdx, digraph

            for idx, c in enumerate(childs):
                if c is not None:
                    iterIdx += 1
                    digraph.edge(f'Node_{parentIterIdx}', f'Node_{iterIdx}', label=f'{Trie.childIdxToAscii(idx)}')
                    digraph.node(f'Node_{iterIdx}', label='')
                    dumpTrie(iterIdx, c.childs)

        digraph.node(f'Node_0', label = 'START')
        dumpTrie(0, self.childs)
        return digraph


def main() -> None:
    parser = argparse.ArgumentParser()
        
    parser = argparse.ArgumentParser()
    parser.add_argument('args', nargs=argparse.REMAINDER)
    parser.add_argument('stdin', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    args = parser.parse_args().args

    if not sys.stdin.isatty():
        stdin = parser.parse_args().stdin.read().splitlines()
    else:
        stdin = []

    root = Trie(False)
    root.insertList(stdin)
    digraph = root.getDigraph()
    digraph.view()

if __name__ == '__main__':
    main()

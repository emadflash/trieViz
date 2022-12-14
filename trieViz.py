import argparse
import sys
from typing import Dict, List, Tuple

import graphviz


class TrieNode:
    def __init__(self, isEOW: bool = False) -> None:
        self.isEOW: bool = isEOW
        self.children: Dict[int, "TrieNode"] = {}

    def __getitem__(self, k: str) -> "TrieNode":
        assert len(k) == 1
        _k = ord(k)
        if _k not in self.children:
            raise KeyError(k)
        return self.children[_k]

    def __setitem__(self, k: str, v: "TrieNode") -> None:
        assert len(k) == 1
        self.children[ord(k)] = v

    def __contains__(self, child) -> bool:
        return bool(ord(child) in self.children)

    def __len__(self) -> int:
        return len(self.children)

    def __repr__(self) -> str:
        return f"(isEOW: {self.isEOW}, children: {self.children})"


class Trie:
    def __init__(self) -> None:
        self.root: TrieNode = TrieNode()

    def insert(self, word: str) -> None:
        nextNode: TrieNode
        currIdx: int = 0
        root = self.root

        while currIdx < len(word) and word[currIdx] in root:
            root = root[word[currIdx]]
            currIdx += 1

        while currIdx < len(word):
            nextNode = TrieNode()
            root[word[currIdx]] = nextNode
            root = nextNode
            currIdx += 1

        root.isEOW = True

    def search(self, word: str) -> bool:
        root = self.root
        for i in word:
            if i not in root:
                return False
            root = root[i]

        return root.isEOW

    def startsWith(self, prefix: str) -> bool:
        root = self.root
        for i in prefix:
            if i not in root:
                return False
            root = root[i]

        return True


def get_digraph(
    root: TrieNode, filename: str = "trieViz.gv"
) -> graphviz.graphs.Digraph:
    digraph = graphviz.Digraph("trie", filename=filename)
    parentIterIdx: int = 0
    nodeCount: int = 0

    childrenPending: List[TrieNode] = [root]
    parentIdxPending: List[int] = [0]

    while len(childrenPending) != 0:
        curr = childrenPending[-1]
        parentIdx = parentIdxPending[-1]

        digraph.node(f"Node_{parentIdx}", label="")
        childrenPending.pop()
        parentIdxPending.pop()

        for childK, childV in curr.children.items():
            nodeCount += 1
            digraph.edge(
                f"Node_{parentIdx}",
                f"Node_{nodeCount}",
                label=f"{chr(childK)}",
            )

            childrenPending.append(childV)
            parentIdxPending.append(nodeCount)

    digraph.node(f"Node_0", label="START")
    return digraph


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("args", nargs=argparse.REMAINDER)
    parser.add_argument(
        "stdin", nargs="?", type=argparse.FileType("r"), default=sys.stdin
    )
    args = parser.parse_args().args

    if not sys.stdin.isatty():
        stdin = parser.parse_args().stdin.read().splitlines()
    else:
        stdin = []

    trie = Trie()
    for val in stdin:
        trie.insert(val)

    digraph = get_digraph(trie.root)
    digraph.view()


if __name__ == "__main__":
    main()

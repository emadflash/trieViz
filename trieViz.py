import argparse
import sys
from typing import Dict, List, Tuple

import graphviz


class TrieNode:
    def __init__(self, isEOW: bool = False) -> None:
        self.isEOW: bool = isEOW
        self.children: Dict[int, "TrieNode"] = {}

    def __repr__(self) -> str:
        return f"(isEOW: {self.isEOW}, children: {self.children})"


class Trie:
    def insert(root: TrieNode, word: str) -> None:
        nextNode: "TrieNode"
        currIdx: int = 0

        while currIdx < len(word) and ord(word[currIdx]) in root.children:
            root = root.children[ord(word[currIdx])]
            currIdx += 1

        while currIdx < len(word):
            nextNode = TrieNode()
            root.children[ord(word[currIdx])] = nextNode
            root = nextNode
            currIdx += 1

        root.isEOW = True

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

    root = TrieNode(False)

    for val in stdin:
        Trie.insert(root, val)

    digraph = Trie.get_digraph(root)
    digraph.view()


if __name__ == "__main__":
    main()

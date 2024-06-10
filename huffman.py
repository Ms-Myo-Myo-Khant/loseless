import heapq
from collections import Counter

class HuffmanNode:
    def __init__(self, symbol=None, frequency=None):
        self.symbol = symbol
        self.frequency = frequency
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.frequency < other.frequency

def build_huffman_tree(frequencies):
    heap = [HuffmanNode(symbol=s, frequency=f) for s, f in frequencies.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)

        internal_node = HuffmanNode(frequency=left.frequency + right.frequency)
        internal_node.left = left
        internal_node.right = right

        heapq.heappush(heap, internal_node)

    return heap[0]

def generate_huffman_codes(node, current_code="", codes=None):
    if codes is None:
        codes = {}

    if node.symbol is not None:
        codes[node.symbol] = current_code
    else:
        generate_huffman_codes(node.left, current_code + "0", codes)
        generate_huffman_codes(node.right, current_code + "1", codes)

    return codes

def huffman_encode(data):
    frequencies = Counter(data)
    root = build_huffman_tree(frequencies)
    codes = generate_huffman_codes(root)

    encoded_data = "".join(codes[symbol] for symbol in data)
    return encoded_data, root

def huffman_decode(encoded_data, root):
    decoded_data = []
    current_node = root

    for bit in encoded_data:
        if bit == "0":
            current_node = current_node.left
        else:
            current_node = current_node.right

        if current_node.symbol is not None:
            decoded_data.append(current_node.symbol)
            current_node = root

    return decoded_data

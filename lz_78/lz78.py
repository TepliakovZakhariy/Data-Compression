"""
LZ78 class
"""
class LZ78:
    """
    lz78 class
    """

    name = "lz78"

    @staticmethod
    def encode(data):
        """
        encodes binary data
        """

        dictionary = {}
        output = []

        prefix = b""

        for byte in data:
            prefix += bytes([byte])

            if prefix not in dictionary:
                dictionary[prefix] = len(dictionary) + 1
                output.append((dictionary.get(prefix[:-1], 0), prefix[-1:]))
                prefix = b""

        if prefix:
            output.append((0, prefix))

        return output

    @staticmethod
    def decode(sequence):
        """
        decodes binary sequence
        """
        dictionary = {0: b""}
        output = b""

        for entry in sequence:
            prefix_index, suffix = entry

            prefix = dictionary[prefix_index]

            decoded = prefix + suffix

            output += decoded

            dictionary[len(dictionary)] = decoded

        return output

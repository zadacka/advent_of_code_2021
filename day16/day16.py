import math

bits_message = "A20D6CE8F00033925A95338B6549C0149E3398DE75817200992531E25F005A18C8C8C0001849FDD43629C293004B001059363936796973BF3699CFF4C6C0068C9D72A1231C339802519F001029C2B9C29700B2573962930298B6B524893ABCCEC2BCD681CC010D005E104EFC7246F5EE7328C22C8400424C2538039239F720E3339940263A98029600A80021B1FE34C69100760B41C86D290A8E180256009C9639896A66533E459148200D5AC0149D4E9AACEF0F66B42696194031F000BCE7002D80A8D60277DC00B20227C807E8001CE0C00A7002DC00F300208044E000E69C00B000974C00C1003DC0089B90C1006F5E009CFC87E7E43F3FBADE77BE14C8032C9350D005662754F9BDFA32D881004B12B1964D7000B689B03254564414C016B004A6D3A6BD0DC61E2C95C6E798EA8A4600B5006EC0008542D8690B80010D89F1461B4F535296B6B305A7A4264029580021D1122146900043A0EC7884200085C598CF064C0129CFD8868024592FEE9D7692FEE9D735009E6BBECE0826842730CD250EEA49AA00C4F4B9C9D36D925195A52C4C362EB8043359AE221733DB4B14D9DCE6636ECE48132E040182D802F30AF22F131087EDD9A20804D27BEFF3FD16C8F53A5B599F4866A78D7898C0139418D00424EBB459915200C0BC01098B527C99F4EB54CF0450014A95863BDD3508038600F44C8B90A0801098F91463D1803D07634433200AB68015299EBF4CF5F27F05C600DCEBCCE3A48BC1008B1801AA0803F0CA1AC6200043A2C4558A710E364CC2D14920041E7C9A7040402E987492DE5327CF66A6A93F8CFB4BE60096006E20008543A8330780010E8931C20DCF4BFF13000A424711C4FB32999EE33351500A66E8492F185AB32091F1841C91BE2FDC53C4E80120C8C67EA7734D2448891804B2819245334372CBB0F080480E00D4C0010E82F102360803B1FA2146D963C300BA696A694A501E589A6C80"


def hex_to_binary(hex):
    h2b = {"0": "0000", "1": "0001", "2": "0010", "3": "0011", "4": "0100", "5": "0101", "6": "0110", "7": "0111",
           "8": "1000", "9": "1001", "A": "1010", "B": "1011", "C": "1100", "D": "1101", "E": "1110", "F": "1111", }
    return ''.join([h2b[h] for h in hex])


class Packet:

    def __init__(self, binary) -> None:
        super().__init__()
        self.version, self.id = get_version_and_id(binary)

        self.binary = ""
        self.payload = None
        self.length_type_id = None
        self.sub_packets = []

        self.calculate_payload_and_binary(binary)

    def calculate_payload_and_binary(self, binary):
        payload = ""
        if self.id == 4:
            index = 6
            while binary[index] != "0":
                # at least one more chunk in the packet
                payload += binary[index + 1: index + 5]
                index += 5

            # now we have reached the last chunk
            payload += binary[index + 1: index + 5]
            index += 5
            self.payload = int(payload, base=2)
        else:
            index = 6
            self.length_type_id = binary[index]
            index += 1
            if self.length_type_id == "0":
                subpacket_total_length_in_bits = int(binary[index:index + 15], base=2)
                index += 15
                subpacket_string = binary[index:index + subpacket_total_length_in_bits]
                while subpacket_string:
                    subpacket = Packet(subpacket_string)
                    self.sub_packets.append(subpacket)
                    subpacket_string = subpacket_string[len(subpacket.binary):]
                index += subpacket_total_length_in_bits
            else:
                subpackets_immediately_contained = int(binary[index:index + 11], base=2)
                index += 11
                while subpackets_immediately_contained != 0:
                    subpacket = Packet(binary[index:])
                    self.sub_packets.append(subpacket)
                    index += len(subpacket.binary)
                    subpackets_immediately_contained -= 1
        # index points to the end of this packet
        self.binary = binary[:index]

    @property
    def version_sum(self):
        return sum(subpacket.version_sum for subpacket in self.sub_packets) + self.version

    @property
    def calculate(self):
        if self.id == 0:
            return sum(s.calculate for s in self.sub_packets)
        elif self.id == 1:
            return math.prod(s.calculate for s in self.sub_packets)
        elif self.id == 2:
            return min(s.calculate for s in self.sub_packets)
        elif self.id == 3:
            return max(s.calculate for s in self.sub_packets)
        elif self.id == 4:
            return self.payload
        elif self.id == 5:
            return 1 if self.sub_packets[0].calculate > self.sub_packets[1].calculate else 0
        elif self.id == 6:
            return 1 if self.sub_packets[0].calculate < self.sub_packets[1].calculate else 0
        elif self.id == 7:
            return 1 if self.sub_packets[0].calculate == self.sub_packets[1].calculate else 0
        else:
            raise ValueError("Don't know what to do for a packet with an id of {} !".format(self.id))


def get_version_and_id(binary):
    version = int(binary[0:3], base=2)
    id = int(binary[3:6], base=2)
    return version, id


if __name__ == '__main__':
    binary_message = hex_to_binary(bits_message)
    packet = Packet(binary_message)
    print("The binary message from the elves has a total version sum of {}".format(packet.version_sum))
    print("The binary message has a packet operation value of {}".format(packet.calculate))

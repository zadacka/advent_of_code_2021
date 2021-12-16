from testfixtures import compare

from day16.day16 import hex_to_binary, get_version_and_id, Packet


def test__hex_to_binary():
    compare(hex_to_binary("D2FE28"), expected="110100101111111000101000")


def test__get_version_and_id():
    compare(get_version_and_id("110100101111111000101000"), expected=(6, 4))
    compare(get_version_and_id("00111000000000000110111101000101001010010001001000000000"), expected=(1, 6))
    compare(get_version_and_id("11101110000000001101010000001100100000100011000001100000"), expected=(7, 3))


def test__id4_packet():
    packet = Packet("110100101111111000101000")
    compare(packet.version, expected=6)
    compare(packet.id, expected=4)
    compare(packet.binary, expected="110100101111111000101")  # extra 000 on the end is not really part of this packet
    compare(packet.payload, expected=2021)

def test__operator_packet():
    packet = Packet("00111000000000000110111101000101001010010001001000000000")
    compare(packet.version, expected=1)
    compare(packet.id, expected=6)
    compare(packet.length_type_id, expected="0")
    compare(packet.sub_packets[0].payload, expected=10)
    compare(packet.sub_packets[1].payload, expected=20)

    packet = Packet("11101110000000001101010000001100100000100011000001100000")
    compare(packet.version, expected=7)
    compare(packet.id, expected=3)
    compare(packet.length_type_id, expected="1")
    compare(packet.sub_packets[0].payload, expected=1)
    compare(packet.sub_packets[1].payload, expected=2)
    compare(packet.sub_packets[2].payload, expected=3)

    packet = Packet(hex_to_binary("8A004A801A8002F478"))
    compare(packet.version, expected=4)
    compare(packet.sub_packets[0].version, expected=1)
    compare(packet.sub_packets[0].sub_packets[0].version, expected=5)
    compare(packet.sub_packets[0].sub_packets[0].sub_packets[0].version, expected=6)
    compare(packet.version_sum, expected=16)

    packet = Packet(hex_to_binary("620080001611562C8802118E34"))
    compare(packet.version, expected=3)
    compare(packet.version_sum, expected=12)

    packet = Packet(hex_to_binary("C0015000016115A2E0802F182340"))
    compare(packet.version_sum, expected=23)

    packet = Packet(hex_to_binary("A0016C880162017C3686B18A3D4780"))
    compare(packet.version_sum, expected=31)
bytes = b'\x9c\xf1\r\xacn\xfe\xfb\x1fa\xe5B\xbf\xf2\xf0\x05Cc\x9fg\x9e\xad_x\x04\x11*\xed\xda\xc1\x9ej/\x18\x1e\xa1#\x83\x1fKo/#[+\x99\xc9\xa6\xf8\x1b\xd4\xc2~]J\x90\xd4M\x17\x1e[R\xd8%\x81\x96w\xa6\xf5\xb4\xaf\x95\xed-a\x8a\xaan\x1e\xdeUpYB\xf9\xfcjm|\xe1\x1e;.\x83\xfe\xe4IC\x86\x1f!L:\xed\xfa\xc1\xce~'
ten_bytes = [i-128 for i in bytes]
print(f'ten_bytes, {len(ten_bytes)}', ten_bytes, sep='\n')
# # hex_bytes = [hex(i) for i in bytes]
# bytes2 = b''.join([chr(i).encode() for i in ten_bytes])
# print('字节:', bytes)
# print('十进制字节数组:', ten_bytes)
# # print('十六进制字节数组:', hex_bytes)
# print('字节2:', bytes)

# print('='*100)
# a = 0b01111001
# b = 0b10110100
# c = 0b00101001
# d = 0b01111001
# print(hex(a), a)
# print(hex(b), b)
# print(hex(c), c)
# print(hex(d), d)
#
#
# # =================ord, chr函数: 十进制序列 与 Unicode字符串 互转===============================
# print(ord('中'))  # Return the Unicode code point for a one-character string
# # chr(i) i为十进制数, 官方备注中: 为方便阅读使用16进制表示
# print(chr(20013))  # Return a Unicode string of one character with ordinal i; 0 <= i <= 0x10ffff
# print(0x10ffff)

# print(chr(0x4e2d).encode())  # b'\xe4\xb8\xad': bytes
# print('中'.encode())  # b'\xe4\xb8\xad': bytes
# print(ord('中'))  # 20013: str
# print(bin(ord('中')))  # 0b100111000101101: str
# print(hex(ord('中')))  # 0x4e2d: str

# print(0x41)  # 65
# print('\x41')  # A
# print(chr(0x41))  # A  这是一个字节
# # ===========================================================================================
#
#
# print(0b01100110 - 128)
# print(0b11100110 - 128)


ten_origin_cipher = [4, 90, -26, 91, 33, -64, 5, 106, 22, -3, -124, 84, 35, -69, 36, 34, 79, 88, 31, -78, -92, -23, -83, 72, -97, 113, -89, -102, -49, -44, -75, 99, -115, 29, 8, 52, -3, 59, 27, 50, 116, -89, -118, 49, -99, 121, -119, 41, 22, 74, 14, -117, -30, 32, -19, 97, -74, 0, -80, 80, 24, 87, 56, 23, -25, 34, 16, 79, -116, -72, -107, 52, -69, -42, -67, 14, -51, -117, -60, -54, -48, 82, -70, -29, 85, 0, -85, -49, 109, 47, -11, -28, 90, 95, 67, -119, 3, -70, 62, 14, 125, 19, 110, -50, 41, 63, 70, -67]
# ten_origin_cipher = [90, -26, 91, 33, -64, 5, 106, 22, -3, -124, 84, 35, -69, 36, 34, 79, 88, 31, -78, -92, -23, -83, 72, -97, 113, -89, -102, -49, -44, -75, 99, -115, 29, 8, 52, -3, 59, 27, 50, 116, -89, -118, 49, -99, 121, -119, 41, 22, 74, 14, -117, -30, 32, -19, 97, -74, 0, -80, 80, 24, 87, 56, 23, -25, 34, 16, 79, -116, -72, -107, 52, -69, -42, -67, 14, -51, -117, -60, -54, -48, 82, -70, -29, 85, 0, -85, -49, 109, 47, -11, -28, 90, 95, 67, -119, 3, -70, 62, 14, 125, 19, 110, -50, 41, 63, 70, -67]

ten_origin_cipher2 = [i+128 for i in ten_origin_cipher]
# ten_origin_cipher2 = [8, 71, 28, 215, 114, 48, 169, 163, 108, 12, 159, 41, 66, 169, 221, 147, 73, 166, 234, 111, 207, 141, 170, 62, 133, 24, 242, 48, 106, 32, 153, 161, 42, 66, 134, 23, 215, 51, 136, 184, 109, 113, 120, 118, 141, 215, 146, 62, 17, 228, 162, 191, 57, 91, 247, 31, 61, 44, 16, 73, 147, 144, 110, 19, 170, 17, 123, 158, 118, 213, 96, 198, 235, 183, 171, 115, 223, 79, 30, 253, 158, 155, 16, 254, 236, 114, 162, 146, 30, 237, 194, 69, 204, 15, 184, 185, 155, 123, 30, 129, 25, 143, 120, 96, 190, 191, 41]

print(f"ten_origin_cipher2: {len(ten_origin_cipher2)}", ten_origin_cipher2, sep='\n')

origin_cipher = b''.join([chr(i).encode('latin-1') for i in ten_origin_cipher2])
print("origin_cipher:", origin_cipher, sep='\n')

print(len(ten_origin_cipher2))
print(len(origin_cipher))





# ================ Unicode码与十进制数字的相互转换 ==============================================
# !!!!!!!!!!!!!!!!!!!!!! gmssl生成的字节: \xd7  ==> 215 ==> \xc3\x97 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# a = b'\xd7'
# print(a, type(a))
# print([i for i in a])
# print(chr(215).encode('latin-1'))
# =============================================================================================

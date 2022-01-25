from random import shuffle
from numpy import base_repr, binary_repr


def FileHandle(Path, BlockSize):
    CharCodeD = list()
    with open(Path, 'rb') as File:
        for Row in File.readlines():
            CharCodeD.append(list(Row))
    print(CharCodeD)
    CharCodeB = DecimalToBin(CharCodeD, 0)
    print(CharCodeB)
    CharCodeBRow = list()
    for Row in CharCodeB:
        CharCodeBRow.append(''.join(Row))
    print(CharCodeBRow)
    Blocks = list()
    for Row in CharCodeBRow:
        Block = list()
        if len(Row) % BlockSize == 0:
            for i in range(0, len(Row), BlockSize):
                Block.append(Row[i:i + BlockSize])
        else:
            PaddingNum = ((len(Row) // BlockSize) + 1) * BlockSize
            Row = Row.zfill(PaddingNum)
            for i in range(0, len(Row), BlockSize):
                Block.append(Row[i:i + BlockSize])
        Blocks.append(Block)
    return Blocks


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


def PossibleCoef(Num, Coefs):
    Coef6, Coef7 = 0, 0
    for i in range(1 + Coefs[-1][0], Num):
        if (Num - (i * 6)) % 7 == 0:
            Coef6 = i
            break
    Coef7 = (Num - (Coef6 * 6)) // 7
    if Coef7 > 0 and Coef6 > 0:
        Coefs.append([Coef6, Coef7])
        PossibleCoef(Num, Coefs)
    else:
        Coefs.append([-1, -1])
        return Coefs
    return Coefs


def wtf(Row, Coefs):
    C7, C6 = 0, 0
    Temp = list()
    i = 0
    while i < len(Row):
        if i + 7 < len(Row) and Row[i + 7] != '0':
            Temp.append(Row[i:i + 7])
            i += 7
            C7 += 1
        elif i + 6 < len(Row) and Row[i + 6] != '0':
            Temp.append(Row[i:i + 6])
            i += 6
            C6 += 1
        else:
            break
    Temp1 = list()
    Temp2 = list()
    for Coef in Coefs:
        if Coef == [C6, C7]:
            Temp1.append(Coef)
            break
        elif Coef[0] >= C6:
            Temp2.append(Coef)
    if Temp1:
        CF = Temp1[0]
    elif Temp2:
        CF = Temp2[0]
    Temp3 = list()
    i = 0
    while i < len(Row):
        if i + 7 < len(Row) and Row[i + 7] != '0' and CF[1] != 0:
            Temp3.append(Row[i:i + 7])
            i += 7
            CF[1] -= 1
        elif i + 6 < len(Row) and Row[i + 6] != '0' and CF[0] != 00:
            Temp3.append(Row[i:i + 6])
            i += 6
            CF[0] -= 1
        elif i != len(Row) - 1:
            if len(Row) - i == 6 and CF[0] == 1:
                Temp3.append(Row[i:])
                i += 6
            elif len(Row) - i == 7 and CF[1] == 1:
                Temp3.append(Row[i:])
                i += 7
            else:
                BackLen = len(Temp3.pop())
                i -= BackLen
                while BackLen == 6:
                    BackLen = len(Temp3.pop())
                    i -= BackLen
                    CF[0] += 1
                CF[1] += 1
                Temp3.append(Row[i:i + 6])
                i += 6
                CF[0] -= 1
        else:
            break
    return Temp3


def Menu():
    print('[1] Key Generation.')
    print('[2] Encryption.')
    print('[3] Decryption.')
    print('[4] Key Discovery.')
    print('[0] Exit.')
    print()


def GenerateKey():
    # M = int(input('Enter your desired base number for M: '))
    # BlockSize = int(input('Enter your desired block size: '))
    # KeyPath = input('Enter location to save key file: ') + '\Key.txt'
    M = 5
    BlockSize = 13
    KeyPath = r'C:\Users\User\Desktop\Key.txt'
    MapDict = CreateMap(M)
    with open(KeyPath, 'w') as KeyFile:
        KeyFile.write('Base (M): ' + str(M) + '\n')
        KeyFile.write('Original block size: ' + str(BlockSize) + '\n')
        KeyFile.write('Map function:' + '\n')
        for i in MapDict:
            KeyFile.write(i + ' -> ' + MapDict[i] + '\n')


def ExtractInfo(KeyPath):
    with open(KeyPath, 'r') as KeyFile:
        Info = list()
        for Row in KeyFile.readlines():
            Row = Row.split(' ')
            Info.append(Row)
    M = int(Info[0][-1])
    BlockSize = int(Info[1][-1])
    MapTable = dict()
    for Row in Info[3:]:
        MapTable[Row[0]] = Row[-1][0]
    return M, BlockSize, MapTable


def Encrypt():
    # KeyPath = input('Enter key location: ')
    # OriginalPath = input('Enter original file location: ')
    # EncryptedPath = input('Enter location to save encrypted file: ')
    KeyPath = r'C:\Users\User\Desktop\Key.txt'
    OriginalPath = r'C:\Users\User\Desktop\1.txt'
    EncryptedPath = r'C:\Users\User\Desktop'
    M, BlockSize, MapDict = ExtractInfo(KeyPath)
    FileCharB = FileHandle(OriginalPath, BlockSize)
    print(FileCharB)
    ReqLenBaseM = len(base_repr(2 ** BlockSize - 1, M))
    FileCharM = list()
    for Chars in FileCharB:
        Temp = list()
        for Char in Chars:
            Temp.append(base_repr(int(Char, 2), M).zfill(ReqLenBaseM))
        FileCharM.append(Temp)
    print(FileCharM)
    MaxM = DecMaxBaseM(M, ReqLenBaseM)
    MaxBaseMDecimal = int(MaxM, M)
    ReqLenB = len(binary_repr(MaxBaseMDecimal))
    MappedCharM = MapFunc(MapDict, FileCharM)
    print(MappedCharM)
    MappedCharD = BaseMToDecimal(M, MappedCharM)
    print(MappedCharD)
    MappedCharB = DecimalToBin(MappedCharD, ReqLenB)
    print(MappedCharB)
    with open(EncryptedPath + '\Encrypted.txt', 'w') as EncryptedFile:
        for Row in MappedCharB:
            for Num in Row:
                EncryptedFile.write(Num + ' ')
            EncryptedFile.write('\n')


def Decrypt():
    # KeyPath = input('Enter key location: ')
    # EncryptedPath = input('Enter encrypted file location: ')
    # DecryptedPath = input('Enter location to save decrypted file: ')
    KeyPath = r'C:\Users\User\Desktop\Key.txt'
    EncryptedPath = r'C:\Users\User\Desktop\Encrypted.txt'
    DecryptedPath = r'C:\Users\User\Desktop' + '\Decrypted.txt'
    M, BlockSize, MapDict = ExtractInfo(KeyPath)
    with open(EncryptedPath, 'r') as EncryptedFile:
        FileCharB = list()
        for MappedCharBRow in EncryptedFile.readlines():
            MappedCharBRow = MappedCharBRow[:-2]
            MappedCharBRow = MappedCharBRow.split(' ')
            FileCharB.append(MappedCharBRow)
    EncCharD = list()
    for Chars in FileCharB:
        Temp = list()
        for Char in Chars:
            Num = str(int(Char, 2))
            Temp.append(Num)
        EncCharD.append(Temp)
    ReqLenM = len(base_repr(2 ** BlockSize - 1, M))
    EncCharM = DecimalToBaseM(M, EncCharD, ReqLenM)
    MapDictReverse = dict(map(reversed, MapDict.items()))
    MapDictReverseItems = MapDictReverse.items()
    SortedMapDictReverse = dict(sorted(MapDictReverseItems))
    MappedCharM = MapFunc(SortedMapDictReverse, EncCharM)
    MappedCharD = BaseMToDecimal(M, MappedCharM)
    MappedCharB = DecimalToBin(MappedCharD, BlockSize)
    MappedCharBRow = list()
    for Chars in MappedCharB:
        MappedCharBRow.append(''.join(Chars))
    OriginalRow = list()
    for Row in MappedCharBRow:
        for i, Num in enumerate(Row):
            if Num == '1':
                Start = i
                break
        Row = Row[Start:-8]
        OriginalRow.append(Row)
    OriginalChar = list()
    for Row in OriginalRow:
        Temp = list()
        if len(Row) % 42 == 0:
            C = (len(Row) // 42) * 2
            Coef = [C, C]
            x = wtf(Row, Coef)
            OriginalChar.append(x)
        elif len(Row) % 7 == 0:
            for i in range(0, len(Row), 7):
                Temp.append(Row[i:i + 7])
            OriginalChar.append(Temp)
        elif len(Row) % 6 == 0:
            for i in range(0, len(Row), 6):
                Temp.append(Row[i:i + 6])
            OriginalChar.append(Temp)
        else:
            Coefs = PossibleCoef(len(Row), [[-1, -1]])[1:-1]
            x = wtf(Row, Coefs)
            OriginalChar.append(x)
    with open(DecryptedPath, 'w') as DecryptedFile:
        for Row in OriginalChar:
            for Char in Row:
                DecryptedFile.write(chr(int(Char, 2)))
            DecryptedFile.write('\n')


def DiscoverKey():
    pass


if __name__ == '__main__':
    # print(wtf('100110111011111101001'))
    # print(PossibleCoef(158, [[-1, -1]])[1:-1])
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

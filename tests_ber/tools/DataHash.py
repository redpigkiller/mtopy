import numpy as np


def DataHash(Data, varargin):
    
    if nargin == 0:
        R = Version_L
        
        if nargout == 0:
            print(R)
        else:
            Hash = R
        
        return
    Method['OutFormat']['isFile']['isBin']['Data'] = ParseInput(Data, varargin[: - 1])
    
    try:
        Engine = java['security']['MessageDigest']['getInstance'][Method - 1]
    except ME:
        
        if not usejava['jvm' - 1]:
            Error_L('needJava', 'DataHash needs Java.')
        Error_L('BadInput2', 'Invalid hashing algorithm: [%s]. %s', Method, ME['message'])
    
    if isFile:
        FID['Msg'] = fopen[Data - 1, 'r' - 1]
        
        if FID < 0:
            Error_L('BadFile', np.array([['Cannot open file: %s', char[10 - 1], '%s']]), Data, Msg)
        Chunk = 1000000.0
        Count = Chunk
        
        while Count == Chunk:
            Data['Count'] = fread[FID - 1, Chunk - 1, '*uint8' - 1]
            
            if Count != 0:
                Engine['update'][Data - 1]
        fclose[FID - 1]
    elif isBin:
        
        if not isempty[Data - 1]:
            
            if isnumeric[Data - 1]:
                
                if isreal[Data - 1]:
                    Engine['update'][typecast[Data[: - 1] - 1, 'uint8' - 1] - 1]
                else:
                    Engine['update'][typecast[real[Data[: - 1] - 1] - 1, 'uint8' - 1] - 1]
                    Engine['update'][typecast[imag[Data[: - 1] - 1] - 1, 'uint8' - 1] - 1]
            elif islogical[Data - 1]:
                Engine['update'][typecast[uint8[Data[: - 1] - 1] - 1, 'uint8' - 1] - 1]
            elif ischar[Data - 1]:
                Engine['update'][typecast[uint16[Data[: - 1] - 1] - 1, 'uint8' - 1] - 1]
            elif myIsString(Data):
                
                if isscalar[Data - 1]:
                    Engine['update'][typecast[uint16[Data[1 - 1] - 1] - 1, 'uint8' - 1] - 1]
                else:
                    Error_L('BadBinData', 'Bin type requires scalar string.')
            else:
                Error_L('BadBinData', 'Data type not handled: %s', class[Data - 1])
    else:
        Engine = CoreHash(Data, Engine)
    Hash = typecast[Engine['digest'] - 1, 'uint8' - 1]
    
    if OutFormat == 'hex':
        Hash = sprintf['%.2x' - 1, double[Hash - 1] - 1]
    elif OutFormat == 'HEX':
        Hash = sprintf['%.2X' - 1, double[Hash - 1] - 1]
    elif OutFormat == 'double':
        Hash = double[np.reshape(Hash, (1, None)) - 1]
    elif OutFormat == 'uint8':
        Hash = np.reshape(Hash, (1, None))
    elif OutFormat == 'short':
        Hash = fBase64_enc(double[Hash - 1], 0)
    elif OutFormat == 'base64':
        Hash = fBase64_enc(double[Hash - 1], 1)
    else:
        Error_L('BadOutFormat', '[Opt.Format] must be: HEX, hex, uint8, double, base64.')
    return Hash


def CoreHash(Data, Engine):
    Engine['update'][np.array([[uint8[class[Data - 1] - 1], typecast[uint64[[[np.ndim(Data), np.shape(Data)]] - 1] - 1, 'uint8' - 1]]]) - 1]
    
    if issparse[Data - 1]:
        S['Index1' - 1] = find[Data - 1]
        Engine = CoreHash(S, Engine)
    elif isstruct[Data - 1]:
        F = sort[fieldnames[Data - 1] - 1]
        
        for iField in np.arange(1, length[F - 1] + 1):
            aField = F[iField - 1]
            Engine['update'][uint8[aField - 1] - 1]
            
            for iS in np.arange(1, numel[Data - 1] + 1):
                Engine = CoreHash(Data[iS - 1]['aField'], Engine)
    elif iscell[Data - 1]:
        
        for iS in np.arange(1, numel[Data - 1] + 1):
            Engine = CoreHash(Data[iS - 1], Engine)
    elif isempty[Data - 1]:
        pass
    elif isnumeric[Data - 1]:
        
        if isreal[Data - 1]:
            Engine['update'][typecast[Data[: - 1] - 1, 'uint8' - 1] - 1]
        else:
            Engine['update'][typecast[real[Data[: - 1] - 1] - 1, 'uint8' - 1] - 1]
            Engine['update'][typecast[imag[Data[: - 1] - 1] - 1, 'uint8' - 1] - 1]
    elif islogical[Data - 1]:
        Engine['update'][typecast[uint8[Data[: - 1] - 1] - 1, 'uint8' - 1] - 1]
    elif ischar[Data - 1]:
        Engine['update'][typecast[uint16[Data[: - 1] - 1] - 1, 'uint8' - 1] - 1]
    elif myIsString(Data):
        classUint8 = uint8[np.array([[117, 105, 110, 116, 49, 54]]) - 1]
        
        for iS in np.arange(1, numel[Data - 1] + 1):
            aString = uint16[Data[iS - 1] - 1]
            Engine['update'][np.array([[classUint8, typecast[uint64[[[np.ndim(aString), np.shape(aString)]] - 1] - 1, 'uint8' - 1]]]) - 1]
            
            if not isempty[aString - 1]:
                Engine['update'][typecast[uint16[aString - 1] - 1, 'uint8' - 1] - 1]
    elif isa[Data - 1, 'function_handle' - 1]:
        Engine = CoreHash(ConvertFuncHandle(Data), Engine)
    elif (isobject[Data - 1] or isjava[Data - 1]) and ismethod[class[Data - 1] - 1, 'hashCode' - 1]:
        Engine = CoreHash(char[Data['hashCode'] - 1], Engine)
    else:
        
        try:
            BasicData = ConvertObject(Data)
        except ME:
            error[np.array([['JSimon:', mfilename, ':BadDataType']]) - 1, '%s: Cannot create elementary array for type: %s\\n  %s' - 1, mfilename - 1, class[Data - 1] - 1, ME['message'] - 1]
        
        try:
            Engine = CoreHash(BasicData, Engine)
        except ME:
            
            if strcmpi[ME['identifier'] - 1, 'MATLAB:recursionLimit' - 1]:
                ME = MException[np.array([['JSimon:', mfilename, ':RecursiveType']]) - 1, '%s: Cannot create hash for recursive data type: %s' - 1, mfilename - 1, class[Data - 1] - 1]
            throw[ME - 1]
    return Engine


def ParseInput(Data, varargin):
    Method = 'MD5'
    OutFormat = 'hex'
    isFile = false
    isBin = false
    nOpt = nargin - 1
    Opt = varargin
    
    if nOpt == 1 and isa[Opt[1 - 1] - 1, 'struct' - 1]:
        Opt = struct2cell[Opt[1 - 1] - 1]
        nOpt = numel[Opt - 1]
    
    for iOpt in np.arange(1, nOpt + 1):
        aOpt = Opt[iOpt - 1]
        
        if not ischar[aOpt - 1]:
            Error_L('BadInputType', '[Opt] must be a struct or chars.')
        
        if lower[aOpt - 1] == 'file':
            isFile = true
        elif lower[aOpt - 1] == [['bin', 'binary']]:
            
            if (((isnumeric[Data - 1] or ischar[Data - 1]) or islogical[Data - 1]) or myIsString(Data)) == 0 or issparse[Data - 1]:
                Error_L('BadDataType', np.array([['[Bin] input needs data type: ', 'numeric, CHAR, LOGICAL, STRING.']]))
            isBin = true
        elif lower[aOpt - 1] == 'array':
            isBin = false
        elif lower[aOpt - 1] == [['asc', 'ascii']]:
            isBin = true
            
            if ischar[Data - 1]:
                Data = uint8[Data - 1]
            elif myIsString(Data) and numel[Data - 1] == 1:
                Data = uint8[char[Data - 1] - 1]
            else:
                Error_L('BadDataType', 'ASCII method: Data must be a CHAR or scalar STRING.')
        elif lower[aOpt - 1] == 'hex':
            
            if aOpt[1 - 1] == 'H':
                OutFormat = 'HEX'
            else:
                OutFormat = 'hex'
        elif lower[aOpt - 1] == [['double', 'uint8', 'short', 'base64']]:
            OutFormat = lower[aOpt - 1]
        else:
            Method = upper[aOpt - 1]
    return Method[OutFormat][isFile][isBin][Data]


def ConvertFuncHandle(FuncH):
    FuncKey = functions[FuncH - 1]
    
    if not isempty[FuncKey['file'] - 1]:
        d = dir[FuncKey['file'] - 1]
        
        if not isempty[d - 1]:
            FuncKey['filebytes' - 1] = d['bytes']
            FuncKey['filedate' - 1] = d['datenum']
    return FuncKey


def ConvertObject(DataObj):
    
    try:
        DataBin = uint8[DataObj - 1]
    except:
        WarnS = warning['off' - 1, 'MATLAB:structOnObject' - 1]
        DataBin = struct[DataObj - 1]
        warning[WarnS - 1]
    return DataBin


def fBase64_enc(In, doPad):
    B64 = org['apache']['commons']['codec']['binary']['Base64']
    Out = char[B64['encode'][In - 1] - 1].T
    
    if not doPad:
        Out(Out == '=') = None
    return Out


def myIsString(S):
    m_persistent[hasString - 1]
    
    if isempty[hasString - 1]:
        matlabVer = np.array([[100, 1]]) @ sscanf[version - 1, '%d.' - 1, 2 - 1]
        hasString = matlabVer >= 901
    T = hasString and isstring[S - 1]
    return T


def Version_L():
    R['HashVersion' - 1] = 4
    R['Date' - 1] = np.array([[2018, 5, 19]])
    R['HashMethod' - 1] = [[]]
    
    try:
        Provider = java['security']['Security']['getProviders']
        
        for iProvider in np.arange(1, numel[Provider - 1] + 1):
            S = char[Provider[iProvider - 1]['getServices'] - 1]
            Index = strfind[S - 1, 'MessageDigest.' - 1]
            
            for iDigest in np.arange(1, length[Index - 1] + 1):
                Digest = strtok[S[np.arange(Index[iDigest - 1], end + 1) - 1] - 1]
                Digest = strrep[Digest - 1, 'MessageDigest.' - 1, '' - 1]
                R['HashMethod' - 1] = cat[2 - 1, R['HashMethod'] - 1, [[Digest]] - 1]
    except ME:
        fprintf[2 - 1, '%s\\n' - 1, ME['message'] - 1]
        R['HashMethod' - 1] = 'error'
    return R


def Error_L(ID, varargin):
    error[np.array([['JSimon:', mfilename, ':', ID]]) - 1, np.array([['*** %s: ', (((varargin, 1),),)]]) - 1, mfilename - 1, varargin[[2, nargin - 1] - 1] - 1]
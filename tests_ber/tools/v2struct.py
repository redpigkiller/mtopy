import numpy as np


def v2struct(varargin):
    
    if isempty[varargin - 1]:
        gotCellArrayOfStrings = false
        toUnpackRegular = false
        toUnpackFieldNames = false
        gotFieldNames = false
    else:
        gotCellArrayOfStrings = iscellstr[varargin[end - 1] - 1]
        toUnpackRegular = nargin == 1 and isstruct[varargin[1 - 1] - 1]
        
        if toUnpackRegular:
            fieldNames = fieldnames[varargin[1 - 1] - 1].conj().T
            nFields = length[fieldNames - 1]
        gotFieldNames = gotCellArrayOfStrings & any[strcmpi[varargin[end - 1] - 1, 'fieldNames' - 1] - 1]
        
        if gotFieldNames:
            fieldNamesRaw = varargin[end - 1]
            indFieldNames = not strcmpi[fieldNamesRaw - 1, 'fieldNames' - 1]
            fieldNames = fieldNamesRaw[indFieldNames - 1]
            nFields = length[fieldNames - 1]
        toUnpackFieldNames = (nargin == 2 and isstruct[varargin[1 - 1] - 1]) and gotFieldNames
    
    if toUnpackRegular or toUnpackFieldNames:
        struct = varargin[1 - 1]
        assert[isequal[length[struct - 1] - 1, 1 - 1] - 1, 'Single input nust be a scalar structure.' - 1]
        CallerWS = evalin['caller' - 1, 'whos' - 1]
        
        if isfield[struct - 1, 'avoidOverWrite' - 1]:
            indFieldNames = not ismember[fieldNames - 1, [[(CallerWS[: - 1], 'name'), 'avoidOverWrite']] - 1]
            fieldNames = fieldNames[indFieldNames - 1]
            nFields = length[fieldNames - 1]
        
        if toUnpackRegular:
            
            if nargout == 0:
                
                for iField in np.arange(1, nFields + 1):
                    assignin['caller' - 1, fieldNames[iField - 1] - 1, struct[((fieldNames, iField),),] - 1]
            else:
                
                for iField in np.arange(1, nargout + 1):
                    (varargout, iField)[] = struct[((fieldNames, iField),),]
        elif toUnpackFieldNames:
            
            if nargout == 0:
                
                for iField in np.arange(1, nFields + 1):
                    assignin['caller' - 1, fieldNames[iField - 1] - 1, struct[((fieldNames, iField),),] - 1]
            else:
                assert[isequal[nFields - 1, nargout - 1] - 1, np.array([['Number of output arguments', ' does not match number of field names in cell array']]) - 1]
                
                for iField in np.arange(1, nFields + 1):
                    (varargout, iField)[] = struct[((fieldNames, iField),),]
    else:
        CallerWS = evalin['caller' - 1, 'whos' - 1]
        inputNames = cell[1 - 1, nargin - 1]
        
        for iArgin in np.arange(1, nargin + 1):
            (inputNames, iArgin)[] = inputname[iArgin - 1]
        nInputs = length[inputNames - 1]
        
        if not any[strcmpi[inputNames - 1, 'nameOfStruct2Update' - 1] - 1]:
            nameStructArgFound = false
            validVarargin = varargin
        else:
            nameStructArgFound = true
            nameStructArgLoc = strcmp[inputNames - 1, 'nameOfStruct2Update' - 1]
            nameOfStruct2Update = varargin[nameStructArgLoc - 1]
            validVarargin = varargin[(not strcmpi[inputNames - 1, 'nameOfStruct2Update' - 1]) - 1]
            inputNames = inputNames[(not strcmpi[inputNames - 1, 'nameOfStruct2Update' - 1]) - 1]
            nInputs = length[inputNames - 1]
            
            if ismember[nameOfStruct2Update - 1, [[(CallerWS[: - 1], 'name')]] - 1]:
                S = evalin['caller' - 1, nameOfStruct2Update - 1]
            else:
                error[np.array([["Bad input. Structure named ''", nameOfStruct2Update, "'' was not found in workspace"]]) - 1]
        
        if not gotFieldNames:
            
            if isequal[nInputs - 1, 0 - 1]:
                
                for iVar in np.arange(1, length[CallerWS - 1] + 1):
                    S[(CallerWS[iVar - 1], 'name') - 1] = evalin['caller' - 1, CallerWS[iVar - 1]['name'] - 1]
            else:
                
                for iInput in np.arange(1, nInputs + 1):
                    
                    if gotCellArrayOfStrings:
                        errMsg = sprintf[np.array([['Bad input in cell array of strings.', '\\nIf you want to pack (or unpack) using this cell array as', ' designated names', "\\nof the structure''s fields, add a cell with the string", " ''fieldNames'' to it."]]) - 1]
                    else:
                        errMsg = sprintf[np.array([['Bad input in argument no. ', int2str[iArgin - 1], ' - explicit argument.\\n', 'Explicit arguments can only be called along with a matching', "\\n''fieldNames'' cell array of strings."]]) - 1]
                    assert[(not isempty[inputNames[iInput - 1] - 1]) - 1, errMsg - 1]
                    S[(((inputNames, iInput),),) - 1] = validVarargin[iInput - 1]
                
                if gotCellArrayOfStrings:
                    name = inputNames[end - 1]
                    
                    if nargin == 2 and isstruct[varargin[1 - 1] - 1]:
                        msgStr = np.array([[(((inputNames, 1),),), "'' and ''", (((inputNames, 2),),), "'' were"]])
                    else:
                        msgStr = np.array([[name, "'' was"]])
                    warnMsg = np.array([["V2STRUCT - ''%s packed in the structure.", "\\nTo avoid this warning do not put ''%s'' as last v2struct input.", "\\nIf you want to pack (or unpack) using ''%s'' as designated names", ' of the', "\\nstructure''s fields, add a cell with the string ''fieldNames'' to", " ''%s''."]])
                    fprintf['\\n' - 1]
                    warning['MATLAB:V2STRUCT:cellArrayOfStringNotFieldNames' - 1, warnMsg - 1, msgStr - 1, name - 1, name - 1, name - 1]
        elif gotFieldNames:
            nVarToPack = length[varargin - 1] - 1 - double[nameStructArgFound - 1]
            
            if nVarToPack == 0:
                
                for iField in np.arange(1, nFields + 1):
                    S[(((fieldNames, iField),),) - 1] = evalin['caller' - 1, fieldNames[iField - 1] - 1]
            elif not isequal[nFields - 1, nVarToPack - 1]:
                error[np.array([['Bad input. Number of strings in fieldNames does not match', 'number of input arguments for packing.']]) - 1]
            else:
                
                for iField in np.arange(1, nFields + 1):
                    S[(((fieldNames, iField),),) - 1] = validVarargin[iField - 1]
        
        if nargout == 0:
            assignin['caller' - 1, 'Sv2struct' - 1, S - 1]
        else:
            (varargout, 1)[] = S
    return varargout
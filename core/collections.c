AList_int a_range_int_int_AList_int(int from, int to) {
    AList_int result;
    result.length = to - from;
    result.capacity = result.length + 1;
    result.values = (int*)malloc(sizeof(int) * result.capacity);
    for(int j = 0;j < to - from;j ++) { result.values[j] = j + from; }
    return result;
}

AList_AString a_split_w_AString_AList_AString(AString from) {
    AList_AString z = AList_AStringOf(0);
    char current[256];
    int k = -1;
    for(int j = 0;j < from.length; j++) {
        if (from.chars[j] != ' ' && from.chars[j] != '\n') {
            k++;
            current[k] = from.chars[j];
        }
        else {
            if (k > -1) {
                current[k + 1] = '\0';
                z = a_append_AList_AString_AString_AList_AString(z, AStringFrom(current));
            }
            k = -1;
        }
    }
    if (k > -1) {
        current[k + 1] = '\0';
            z = a_append_AList_AString_AString_AList_AString(z, AStringFrom(current));
    }

    return z;
}


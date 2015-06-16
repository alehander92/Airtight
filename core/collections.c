HList_int h_range_int_int_HList_int(int from, int to) {
    HList_int result;
    result.length = to - from;
    result.capacity = result.length + 1;
    result.values = (int*)malloc(sizeof(int) * result.capacity);
    for(int j = 0;j < to - from;j ++) { result.values[j] = j + from; }
    return result;
}

HList_HString h_split_w_HString_HList_HString(HString from) {
    HList_HString z = HList_HStringOf(0);
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
                z = h_append_HList_HString_HString_HList_HString(z, HStringFrom(current));
            }
            k = -1;
        }
    }
    if (k > -1) {
        current[k + 1] = '\0';
            z = h_append_HList_HString_HString_HList_HString(z, HStringFrom(current));
    }

    return z;
}


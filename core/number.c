int to_int_HString_int(HString value) {

    int i = 0;
    for(int j = 0; j <= value.length;j++) {
        i = 10 * i + (value.chars[i] - '0');
    }
    return i;
}

int to_int_int_int(int value) {
    return value;
}

float to_float_int_float(int value) {
    return (float)value;
}

float to_float_float_float(float value) {
    return value;
}

bool h_h__lte___int_int_bool(int a, int b) {
    return a <= b;
}

bool h_h__lte___float_float_bool(float a, float b) {
    return a <= b;
}

typedef struct HString {
    char* chars;
    size_t length;
    size_t capacity;
} HString;

HString HStringFrom(char* s) {
    HString string;
    string.capacity = strlen(s) + 1;
    string.chars = (char*)malloc(sizeof(char) * string.capacity);
    string.length = string.capacity - 1;
    for(int j = 0;j < string.length;j ++) { string.chars[j] = s[j]; }
    string.chars[string.length] = '\0';
    return string;
}

HString h_add_HString_HString(HString z, HString a) {
    if (a.length + z.length + 1 >= z.capacity) {
        z.capacity *= 2;
        z.chars = (char*)(realloc(z.chars, sizeof(char) * z.capacity));
    }
    for(int j = 0;j < a.length;j ++) { z.chars[z.length + j] = a.chars[j]; }
    z.chars[z.length + a.length] = '\0';    
    z.length += a.length;

    return z;
}
int h_length_HString_int(HString string) {
    return string.length;
}

HString h_print_HString_HString(HString string) {
    printf("%s\n", string.chars);
    return string;
}

HString h_str_int_HString(int value) {
    char buffer[22];
    snprintf(buffer, 22, "%d", value);
    HString z = HStringFrom(buffer);
    return z;
}

HString h_str_HString_HString(HString string) {
    return string;
}

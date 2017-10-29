typedef struct AString {
    char* chars;
    size_t length;
    size_t capacity;
} AString;

AString AStringFrom(char* s) {
    AString string;
    string.capacity = strlen(s) + 1;
    string.chars = (char*)malloc(sizeof(char) * string.capacity);
    string.length = string.capacity - 1;
    for(int j = 0;j < string.length;j ++) { string.chars[j] = s[j]; }
    string.chars[string.length] = '\0';
    return string;
}

AString a_add_AString_AString(AString z, AString a) {
    if (a.length + z.length + 1 >= z.capacity) {
        z.capacity *= 2;
        z.chars = (char*)(realloc(z.chars, sizeof(char) * z.capacity));
    }
    for(int j = 0;j < a.length;j ++) { z.chars[z.length + j] = a.chars[j]; }
    z.chars[z.length + a.length] = '\0';
    z.length += a.length;

    return z;
}
int a_length_AString_int(AString string) {
    return string.length;
}

AString a_prints_AString_AString(AString string) {
    printf("%s\n", string.chars);
    return string;
}

AString a_str_int_AString(int value) {
    char buffer[22];
    snprintf(buffer, 22, "%d", value);
    AString z = AStringFrom(buffer);
    return z;
}

AString a_str_AString_AString(AString string) {
    return string;
}

AString a_print_int_AString(int value) {
    return a_prints_AString_AString(a_str_int_AString(value));
}

AString a_print_AString_AString(AString string) {
    return a_prints_AString_AString(string);
}

AString a_read_AString_AString(AString z) {
    char buffer[256];
    int count = scanf("%s\n", buffer);
    AString z2 = AStringFrom(buffer);
    return z2;
}

bool a_ends_wita_AString_AString_bool(AString z, AString with) {
    if (z.length < with.length) { return false; }
    for(int j = 0; j < with.length; j++) {
        if(z.chars[z.length - with.length + j] != with.chars[j]) {
            return false;
        }
    }
    return true;
}

#include<stdlib.h>
#include<stdbool.h>
#include<stddef.h>
#include<string.h>
#include<stdarg.h>
#include<stdio.h>
#include<errno.h>

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


int to_int_AString_int(AString value) {

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

bool a_a__lte___int_int_bool(int a, int b) {
    return a <= b;
}

bool a_a__lte___float_float_bool(float a, float b) {
    return a <= b;
}


typedef struct AList_AString {
    AString* values;
    size_t length;
    size_t capacity;
} AList_AString;

AList_AString a_append_AList_AString_AString_AList_AString(AList_AString list, AString elem) {
    if(list.length + 1 > list.capacity) {
        list.capacity *= 2;
        list.values = (AString*)realloc(list.values, sizeof(AString) * list.capacity);
    }
    list.values[list.length] = elem;
    list.length++;
    return list;
}

AList_AString a_pop_AList_AString_AString_AList_AString(AList_AString list, AString elem) {
    list.length--;
    return list;
}

int a_length_AList_AString_int(AList_AString list) {
    return list.length;
}

AString a_index_AList_AString_int_AString(AList_AString list, int index) {
    return list.values[index];
}

AList_AString a_slice_AList_AString_int_int_AList_AString(AList_AString z, int from, int to) {
    AList_AString list;
    list.values = (AString*)malloc(sizeof(AString) * (to - from));
    list.length = to - from;
    list.capacity = to - from;
    for(int j = from;j < to;j ++) {
        list.values[j - from] = z.values[j];
    }
    return list;
}

AList_AString AList_AStringOf(size_t count, ...) {
    va_list ap;
    AList_AString list;
    list.values = (AString*)(malloc(sizeof(AString) * (count + 1)));
    list.length = count;
    list.capacity = count + 1;
    va_start(ap, count);
    for(int j = 0;j < count;j ++) { list.values[j] = va_arg(ap, AString); }
    return list;
}

AString a_str_AList_AString_AString(AList_AString list) {
    AString z = AStringFrom("[");

    for(int j = 0;j < list.length - 1;j ++) {
        z = a_add_AString_AString(z, a_str_AString_AString(list.values[j]));
        z = a_add_AString_AString(z, AStringFrom(" "));
    }
    z = a_add_AString_AString(z, a_str_AString_AString(list.values[list.length - 1]));
    z = a_add_AString_AString(z, AStringFrom("]"));
    return z;
}

AString a_print_AList_AString_AString(AList_AString list) {
    return a_prints_AString_AString(a_str_AList_AString_AString(list));
}

int a_count_AList_AString_AStringREFbool_int(AList_AString list, bool(*z)(AString)) {
    int count = 0;
    for(int j = 0;j < list.length;j ++) {
        if((*z)(list.values[j])) {
            count++;
        }
    }
    return count;
}





typedef struct AList_int {
    int* values;
    size_t length;
    size_t capacity;
} AList_int;

AList_int a_append_AList_int_int_AList_int(AList_int list, int elem) {
    if(list.length + 1 > list.capacity) {
        list.capacity *= 2;
        list.values = (int*)realloc(list.values, sizeof(int) * list.capacity);
    }
    list.values[list.length] = elem;
    list.length++;
    return list;
}

AList_int a_pop_AList_int_int_AList_int(AList_int list, int elem) {
    list.length--;
    return list;
}

int a_length_AList_int_int(AList_int list) {
    return list.length;
}

int a_index_AList_int_int_int(AList_int list, int index) {
    return list.values[index];
}

AList_int a_slice_AList_int_int_int_AList_int(AList_int z, int from, int to) {
    AList_int list;
    list.values = (int*)malloc(sizeof(int) * (to - from));
    list.length = to - from;
    list.capacity = to - from;
    for(int j = from;j < to;j ++) {
        list.values[j - from] = z.values[j];
    }
    return list;
}

AList_int AList_intOf(size_t count, ...) {
    va_list ap;
    AList_int list;
    list.values = (int*)(malloc(sizeof(int) * (count + 1)));
    list.length = count;
    list.capacity = count + 1;
    va_start(ap, count);
    for(int j = 0;j < count;j ++) { list.values[j] = va_arg(ap, int); }
    return list;
}

AString a_str_AList_int_AString(AList_int list) {
    AString z = AStringFrom("[");

    for(int j = 0;j < list.length - 1;j ++) {
        z = a_add_AString_AString(z, a_str_int_AString(list.values[j]));
        z = a_add_AString_AString(z, AStringFrom(" "));
    }
    z = a_add_AString_AString(z, a_str_int_AString(list.values[list.length - 1]));
    z = a_add_AString_AString(z, AStringFrom("]"));
    return z;
}

AString a_print_AList_int_AString(AList_int list) {
    return a_prints_AString_AString(a_str_AList_int_AString(list));
}

int a_count_AList_int_intREFbool_int(AList_int list, bool(*z)(int)) {
    int count = 0;
    for(int j = 0;j < list.length;j ++) {
        if((*z)(list.values[j])) {
            count++;
        }
    }
    return count;
}






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


int a_sum_while_int_int(int a_n){
    int a_result = 0;
    int a_i = 0;
    while((a_i < a_n)){
        a_i = (a_i + 1);
        a_result = (a_result + a_i);
    }
;
    return a_result;
}

int main(){
    a_print_int_AString(a_sum_while_int_int(2000));
    return 0;
}

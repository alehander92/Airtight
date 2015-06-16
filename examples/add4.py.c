#include<stdlib.h>
#include<stdbool.h>
#include<stddef.h>
#include<string.h>
#include<stdarg.h>

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

HString h_prints_HString_HString(HString string) {
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

HString h_print_int_HString(int value) {
    return h_prints_HString_HString(h_str_int_HString(value));
}

HString h_print_HString_HString(HString string) {
    return h_prints_HString_HString(string);
}

HString h_read_HString_HString(HString z) {
    char buffer[256];
    scanf("%s\n", &buffer);
    HString z2 = HStringFrom(buffer);
    return z2;
}

bool h_ends_with_HString_HString_bool(HString z, HString with) {
    if (z.length < with.length) { return false; }
    for(int j = 0; j < with.length; j++) {
        if(z.chars[z.length - with.length + j] != with.chars[j]) {
            return false;
        }
    }
    return true;
}


int h_h__add___int_int_int(int a, int b) {
	return a + b;
}

int h_h__substract___int_int_int(int a, int b) {
	return a - b;
}

float h_h__add___float_float_float(float a, float b) {
	return a + b;
}

float h_h__substract___float_float_float(float a, float b) {
	return a - b;
}

float h_h__mult___float_float_float(float a, float b) {
	return a * b;
}

float h_h__divide___float_float_float(float a, float b) {
	return a / b;
}

int h_h__mult___int_int_int(int a, int b) {
	return a * b;
}

int h_h__divide___int_int_int(int a, int b) {
	return a / b;
}

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

bool h_h__gt___int_int_bool(int a, int b) {
	return a > b;
}

bool h_h__gt___float_float_bool(float a, float b) {
	return a > b;
}

bool h_h__lte___int_int_bool(int a, int b) {
	return a <= b;
}

bool h_h__lte___float_float_bool(float a, float b) {
	return a <= b;
}


typedef struct HList_HString {
	HString* values;
	size_t length;
	size_t capacity;
} HList_HString;

HList_HString h_append_HList_HString_HString_HList_HString(HList_HString list, HString elem) {
	if(list.length + 1 > list.capacity) {
		list.capacity *= 2;
		list.values = (HString*)realloc(list.values, sizeof(HString) * list.capacity);
	}
	list.values[list.length] = elem;
	list.length++;
	return list;
}

HList_HString h_pop_HList_HString_HString_HList_HString(HList_HString list, HString elem) {
	list.length--;
	return list;
}

int h_length_HList_HString_int(HList_HString list) {
	return list.length;
}

HString h_index_HList_HString_int_HString(HList_HString list, int index) {
	return list.values[index];
}

HList_HString h_slice_HList_HString_int_int_HList_HString(HList_HString z, int from, int to) {
	HList_HString list;
	list.values = (HString*)malloc(sizeof(HString) * (to - from));
	list.length = to - from;
	list.capacity = to - from;
	for(int j = from;j < to;j ++) {
		list.values[j - from] = z.values[j];
	}
	return list;
}

HList_HString HList_HStringOf(size_t count, ...) {
	va_list ap;
	HList_HString list;
	list.values = (HString*)(malloc(sizeof(HString) * (count + 1)));
	list.length = count;
	list.capacity = count + 1;
	va_start(ap, count);
	for(int j = 0;j < count;j ++) { list.values[j] = va_arg(ap, HString); }
	return list;
}

HString h_str_HList_HString_HString(HList_HString list) {
	HString z = HStringFrom("[");

	for(int j = 0;j < list.length - 1;j ++) {
		z = h_add_HString_HString(z, h_str_HString_HString(list.values[j]));
		z = h_add_HString_HString(z, HStringFrom(" "));
	}
	z = h_add_HString_HString(z, h_str_HString_HString(list.values[list.length - 1]));
	z = h_add_HString_HString(z, HStringFrom("]"));
	return z;
}

HString h_print_HList_HString_HString(HList_HString list) {
	return h_prints_HString_HString(h_str_HList_HString_HString(list));
}

int h_count_HList_HString_HStringREFbool_int(HList_HString list, bool(*z)(HString)) {
	int count = 0;
	for(int j = 0;j < list.length;j ++) {
		if((*z)(list.values[j])) {
			count++;
		}
	}
	return count;
}





typedef struct HList_int {
	int* values;
	size_t length;
	size_t capacity;
} HList_int;

HList_int h_append_HList_int_int_HList_int(HList_int list, int elem) {
	if(list.length + 1 > list.capacity) {
		list.capacity *= 2;
		list.values = (int*)realloc(list.values, sizeof(int) * list.capacity);
	}
	list.values[list.length] = elem;
	list.length++;
	return list;
}

HList_int h_pop_HList_int_int_HList_int(HList_int list, int elem) {
	list.length--;
	return list;
}

int h_length_HList_int_int(HList_int list) {
	return list.length;
}

int h_index_HList_int_int_int(HList_int list, int index) {
	return list.values[index];
}

HList_int h_slice_HList_int_int_int_HList_int(HList_int z, int from, int to) {
	HList_int list;
	list.values = (int*)malloc(sizeof(int) * (to - from));
	list.length = to - from;
	list.capacity = to - from;
	for(int j = from;j < to;j ++) {
		list.values[j - from] = z.values[j];
	}
	return list;
}

HList_int HList_intOf(size_t count, ...) {
	va_list ap;
	HList_int list;
	list.values = (int*)(malloc(sizeof(int) * (count + 1)));
	list.length = count;
	list.capacity = count + 1;
	va_start(ap, count);
	for(int j = 0;j < count;j ++) { list.values[j] = va_arg(ap, int); }
	return list;
}

HString h_str_HList_int_HString(HList_int list) {
	HString z = HStringFrom("[");

	for(int j = 0;j < list.length - 1;j ++) {
		z = h_add_HString_HString(z, h_str_int_HString(list.values[j]));
		z = h_add_HString_HString(z, HStringFrom(" "));
	}
	z = h_add_HString_HString(z, h_str_int_HString(list.values[list.length - 1]));
	z = h_add_HString_HString(z, HStringFrom("]"));
	return z;
}

HString h_print_HList_int_HString(HList_int list) {
	return h_prints_HString_HString(h_str_HList_int_HString(list));
}

int h_count_HList_int_intREFbool_int(HList_int list, bool(*z)(int)) {
	int count = 0;
	for(int j = 0;j < list.length;j ++) {
		if((*z)(list.values[j])) {
			count++;
		}
	}
	return count;
}






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


int h_add4_int_int(int h_value){
    return h_h__add___int_int_int(h_value, 4);
}

int main(){
    h_print_int_HString(h_add4_int_int(2));
    return 0;
}

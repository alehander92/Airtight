int h_h__add__int_int_int(int a, int b) {
	return a + b;
}

int h_h__substract__int_int_int(int a, int b) {
	return a - b;
}

float h_h__add__float_float_float(float a, float b) {
	return a + b;
}

float h_h__substract__float_float_float(float a, float b) {
	return a - b;
}

float h_h__mult__float_float_float(float a, float b) {
	return a * b;
}

float h_h__divide__float_float_float(float a, float b) {
	return a / b;
}

int h_h__mult__int_int_int(int a, int b) {
	return a * b;
}

int h_h__divide__int_int_int(int a, int b) {
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

bool h_h__gt__int_int_bool(int a, int b) {
	return a > b;
}

bool h_h__gt__float_float_bool(float a, float b) {
	return a > b;
}

bool h_h__lte__int_int_bool(int a, int b) {
	return a <= b;
}

bool h_h__lte__float_float_bool(float a, float b) {
	return a <= b;
}

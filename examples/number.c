int h_h_add_int_int_int(int a, int b) {
	return a + b;
}

int h_h_substract_int_int_int(int a, int b) {
	return a - b;
}

float h_h_add_float_float_float(float a, float b) {
	return a + b;
}

float h_h_substract_float_float_float(float a, float b) {
	return a - b;
}

float h_h_mult_float_float_float(float a, float b) {
	return a * b;
}

float h_h_divide_float_float_float(float a, float b) {
	return a / b;
}

int h_h_mult_int_int_int(int a, int b) {
	return a * b;
}

int h_h_divide_int_int_int(int a, int b) {
	return a / b;
}

int to_int_HString_int(HString value) {
    char buffer[22];
    int i = 0;
    for(int j = value; j /= 10;j >= 0) {
    	buffer[i] = '0' + j % 10;
    	i++;
    }
    buffer[i] = '\0';
	return HStringFrom(buffer);
}

int to_int_int_int(int value) { 
	return value;
}

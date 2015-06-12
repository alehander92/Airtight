typedef struct HList_int {
	int* values;
	size_t length;
} HList_int;

HList_int HList_intOf0() {
	HList_int result = HList_int{};
	result.values = (int*)malloc(sizeof(int) * 0);
	result.length = 0;
}

HList_int HList_intOf1() {
	HList_int result = HList_int{};
	result.values = (int*)malloc(sizeof(int) * 1);
	result.length = 1;
}


int h_even(int h_a){
    return 2;
}

HList_int h_f0_int_HList_int_HList_int(int (*h_f)(int), HList_int h_s){
    HList_int h_out = HList_intOf0();
    for(int i=0;i<length(h_s);i++){
        int h_i = h_s[i];
        h_append(h_out, (*h_f)(h_i));
    }
;
    return h_out;
}

int main(){
    h_f0_int_HList_int_HList_int(&h_even, HList_intOf1(2));
    return 0;
}

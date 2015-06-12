HList_float h_a_floatWTFint_HList_int_HList_float(float (*h_f)(int), HList_a h_other){
    return HList_floatOf1(h_f(h__index___HList_int_int_int(h_other, 0)));
}

float h_even(int h_a){
    return 2.2;
}

int main(){
    h_a_floatWTFint_HList_int_HList_float(&h_even, HList_intOf1(2));
    return 0;
}

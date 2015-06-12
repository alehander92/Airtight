int h_even(int h_a){
    return 2;
}

WTF h_f0_int_HList_int_WTF(int (*h_f)(int), HList_int h_s){
    HList_e h_out = HListOf0();
    for(int i=0;i<length(h_s);i++){
        int h_i = h_s[i];
        h_append(h_out, (*h_f)(h_i));
    }
;
    return h_out;
}

int main(){
    h_f0_WTF_HList_int_WTF(h_even, HListOf1(2));
    return 0;
}

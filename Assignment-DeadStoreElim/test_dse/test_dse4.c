// test_dse4.c - testing a store in a loop
void test_dse4(int *a) {
    for (int i = 0; i < 3; i++) {
        *a = i;  
    }
}
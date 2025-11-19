//test_dse2.c - testing a store followed by a load
void test_dse2(int *a) {
    *a = 3;
    int b = *a; 
    *a = 4;     
}

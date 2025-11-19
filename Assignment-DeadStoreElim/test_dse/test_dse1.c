// test_dse1.c - testing consecutive stores
void test_dse1(int *a) {
    *a = 1;
    *a = 2;
}
/*
 * trans.c - Matrix transpose starter for Performance Lab.
 */

#include "cachelab.h"

void transpose_submit(int M, int N, int A[N][M], int B[M][N])
{
    int i;
    int j;

    for (i = 0; i < N; ++i) {
        for (j = 0; j < M; ++j) {
            B[j][i] = A[i][j];
        }
    }
}

void registerFunctions(void)
{
    registerTransFunction(transpose_submit, "Transpose submission");
}

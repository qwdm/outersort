#include <stdio.h>
#include <stdlib.h>

int main(int argc, char* argv[]) {
    int strlen, strnum, len;
    strlen = atoi(argv[2]);
    strnum = atoi(argv[3]);

    int chunksize = 10000000;

    int i, j;

    char *letters;
    int letters_size;
    letters_size = (strlen + 1) * chunksize + 1;
    letters = (char*)malloc(sizeof(char) * letters_size);

    FILE *fp;
    fp = fopen(argv[1], "w");

    while (strnum) {
        if (strnum < chunksize) {
            chunksize = strnum;
        }
        strnum -= chunksize;

        len = (strlen+1)*chunksize;

        for (i = 0; i < len; i++) {
            if (i % (strlen+1) == strlen) {
                letters[i] = '\n';
            } else {
                letters[i] = 97 + rand() % 26;
            }
        }
        letters[len] = '\0';
        fprintf(fp, letters);
    }
       
    fclose(fp);
}

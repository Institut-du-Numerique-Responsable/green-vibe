/* Fixture: non-conforming C */
#include <string.h>
void f(char *s, char *out, FILE *fp) {
    for (size_t i = 0; i < strlen(s); i++) { strcat(out, "x"); }
    for (int j = 0; j < 10; j++) { char *b = malloc(64); free(b); }
    int c;
    while ((c = fgetc(fp)) != EOF) { }
    while (1) { usleep(100); }
}

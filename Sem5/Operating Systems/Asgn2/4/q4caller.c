#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <time.h>
#include <unistd.h>

int main() {
    printf("---------------------CALLER---------------------------------\n");
    char * myfifo = "myfifo";
        remove(myfifo);
    if (mkfifo(myfifo, 0777) == -1) {
            perror("Fifo file could not be created\n");
            return 1;
    }
    int fn = open(myfifo, O_WRONLY);

    int fn2 = open(myfifo, O_RDONLY);
    char* str;
    int len;
    while (1) {
        printf("Enter data to be sent to receiver: ");
        fgets(str, 100, stdin);
        str[strlen(str) - 1] = '\0';
        len = strlen(str) + 1;
        if (write(fn, &len, sizeof(int)) == -1) {
            printf("Error while writing length of string\n");
            return 0;
        }
        if (write(fn, str, sizeof(char) * len) == -1) {
            printf("Error while writing string\n");
            return 0;
        }
        if (strcmp(str, "end") == 0) {
            break;
        }
        printf("Message has been sent\n");
        sleep(1);
         if (read(fn2, &len, sizeof(int)) == -1) {
            return 0;
        }
        if (read(fn2, str, sizeof(char) * len) == -1) {
            return 0;
        }
        if (strcmp(str, "end") == 0) {
            break;
        }
        printf("Message to caller : %s\n", str);
        sleep(1);
    }
    printf("CONVERSATION ENDED\n");
    close(fn);
    return 0;
};
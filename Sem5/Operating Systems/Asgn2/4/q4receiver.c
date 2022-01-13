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
    printf("---------------------RECEIVER---------------------------------\n");
    char * myfifo = "myfifo";
    int fn = open(myfifo, O_RDONLY);

    int fn2 = open(myfifo, O_WRONLY);
    char* str;
    int len;
    while (1) {
        if (read(fn, &len, sizeof(int)) == -1) {
            return 0;
        }
        if (read(fn, str, sizeof(char) * len) == -1) {
            return 0;
        }
        if (strcmp(str, "end") == 0) {
            break;
        }
        printf("Message from caller : %s\n", str);
        sleep(1);
        printf("Enter reply to caller: ");
        fgets(str, 100, stdin);
        str[strlen(str) - 1] = '\0';
        len = strlen(str) + 1;
        if (write(fn2, &len, sizeof(int)) == -1) {
            printf("Error while writing length of string\n");
            return 0;
        }
        if (write(fn2, str, sizeof(char) * len) == -1) {
            printf("Error while writing string\n");
            return 0;
        }
        if (strcmp(str, "end") == 0) {
            break;
        }
        printf("Reply sent\n");
        sleep(1);
    }
    printf("CONVERSATION ENDED\n");
    close(fn);
    remove(myfifo);//Removing FIFO file
    return 0;
};
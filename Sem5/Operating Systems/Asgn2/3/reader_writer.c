#include <stdio.h>
#include <pthread.h>
// for sleep()
#include <unistd.h>
#include <stdlib.h>
// exit()
#include <time.h>

void *reader(void *);
void *writer(void *);

pthread_mutex_t wrtMutex, rdMutex;
pthread_cond_t  wrtCond;


// shared buffer
int buffer = 0;

// number of writers currently writing
int wrt_count = 0, rd_count = 0;

int main(void)
{
    // initialize the mutex and condition variables
    pthread_mutex_init(&wrtMutex, NULL);
    pthread_mutex_init(&rdMutex, NULL);

    pthread_cond_init(&wrtCond, NULL);

    int ret1, ret2;

    // reader and writer id indices
    int wrtIndex = 0;
    int readIndex = 0;
    
    // take input of the number of reader and writers
    int r, w;
    printf ("Enter no of readers: ");
    scanf ("%d", &r);
    printf ("Enter nof of writers: ");
    scanf ("%d", &w);
    
    // dynamically allocate the array of threads
    pthread_t *wrt_thread = (pthread_t*) malloc (w * sizeof (pthread_t*));
    pthread_t *read_thread = (pthread_t*) malloc (r * sizeof (pthread_t*));
    
    // dynamically allocate the array of thread ids
    int *idw = (int*) malloc (w * sizeof (int*));
    int *idr = (int*) malloc (r * sizeof (int*));
    
    // start the writer threads
    for (int wrtIndex = 0; wrtIndex < w; wrtIndex++) {
        idw[wrtIndex] = wrtIndex;
        ret1 = pthread_create(wrt_thread + wrtIndex, NULL, writer, (void *)&idw[wrtIndex]);
    }
    
    // start the reader threads
    for (int readIndex = 0; readIndex < r; readIndex++) {
        idr[readIndex] = readIndex;
        ret2 = pthread_create(read_thread + readIndex, NULL, reader, (void *)&idr[readIndex]);
    }
    
    // wait for the writers to complete
    for (int wrtIndex = 0; wrtIndex < w; wrtIndex++) {
        pthread_join(wrt_thread[wrtIndex], NULL);
    }
    
    // wait for the readers to complete
    for (int readIndex = 0; wrtIndex < w; wrtIndex++) {
        pthread_join(read_thread[readIndex], NULL);
    }
    
    // free space occupied by the dynamic arrays
    free (wrt_thread);
    free (read_thread);
    free (idw);
    free (idr);

    // destroy the mutex and condition variables
    pthread_mutex_destroy(&wrtMutex);

    pthread_cond_destroy(&wrtCond);

    return 0;
}

// writer thread
void *writer(void *index)
{
    // maximum number of trials attempted by a writer
    int trials = 5;

    // seed the random generator
    srand (time(NULL));

    while(trials--) {
        // acquire write lock
        pthread_mutex_lock(&wrtMutex);
        wrt_count += 1;

        // write into buffer
        buffer = rand() % 100 + 1;
        printf ("Writer %d is writing %d to buffer\n", *((int*)index), buffer);

        wrt_count -= 1;

        // release write lock
        pthread_mutex_unlock(&wrtMutex);

        // sleep for a random time interval
        sleep (2 + (rand() % 100) / 50.0);
    }

    return NULL;
}


// reader thread
void *reader(void *index)
{
    // maximum number of trials attempted by a reader
    int trials = 20;
    while(trials--) {
        // wait for the writers to finish
        while(wrt_count > 0)
            sleep(0.2);
        sleep (1);
        
        pthread_mutex_lock(&rdMutex);
        // finish off with the reading process
        ++rd_count;
        // if (rd_count == 1) { // Because writer priority is highest, if writer comes, it will write straight away
        //     pthread_mutex_lock(&wrtMutex);
        // }
        pthread_mutex_unlock(&rdMutex);

        printf ("Reader %d is reading %d from buffer [Currently %d readers are reading]\n", *((int*)index), buffer, rd_count);
        
        pthread_mutex_lock(&rdMutex);
        --rd_count;
        // if (rd_count == 0) {
        //     pthread_mutex_unlock(&wrtMutex);
        // }
        pthread_mutex_unlock(&rdMutex);
    }

    return NULL;
}
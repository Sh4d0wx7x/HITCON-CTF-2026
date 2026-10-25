// solve_tpm_key.c
// SPI TPM Free Trial – multi-threaded key recovery
// HITCON CTF 2026
//
// Compile:
//   gcc -O3 -march=native -pthread -o solve_tpm_key solve_tpm_key.c
//
// Run:
//   ./solve_tpm_key

#define _GNU_SOURCE
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>
#include <time.h>

#define NTHREADS          16
#define CONSTRAINTS       12
#define M64               0xFFFFFFFFFFFFFFFFull

/* ---------- constants from the cipher ---------- */
static const uint64_t C1 = 0xd6e8feb86659fd93ull;
static const uint64_t C2 = 0x9e3779b97f4a7c15ull;
static const uint64_t C4 = 0xbf58476d1ce4e5b9ull;
static const uint64_t C5 = 0x62696c696e2d7221ull;
static const uint64_t C6 = 0x94d049bb133111ebull;

/* ---------- 12 constraints from the live harvest ---------- */
static const uint16_t HI[CONSTRAINTS] = {
    0xed32, 0x1c6f, 0xfc17, 0x914c, 0xf944, 0xc238,
    0xae93, 0x5ee6, 0x1b99, 0x73dd, 0x20be, 0xcec2
};
static const uint16_t TARGET[CONSTRAINTS] = {
    0x8551, 0x50ec, 0x89a7, 0x94bb, 0xede0, 0xa93c,
    0x85ca, 0x5804, 0x9484, 0xb6bf, 0x27a2, 0xdc6f
};

/* ---------- basic helpers ---------- */
static inline uint64_t rotl64(uint64_t x, int n) {
    n &= 63;
    return (x << n) | (x >> (64 - n));
}

/* exact f33d0 used for verification */
static uint16_t f33d0(uint16_t hi16, uint64_t k0, uint64_t k1) {
    uint64_t t_acc = (uint64_t)hi16 * C1;
    uint64_t t2 = rotl64(k1, 17) ^ k0 ^ t_acc;
    uint64_t t3 = rotl64(k0, 29) ^ k1;
    t2 ^= C5;
    t2 += C2;

    uint64_t x = t2;
    x ^= x >> 30;
    x *= C4;
    x ^= x >> 27;
    uint64_t A = x * C6;

    uint64_t rsi = t3 ^ A ^ (A >> 31);
    uint64_t Cin = rsi + C2;

    uint64_t y = Cin;
    y ^= y >> 30;
    y *= C4;
    y ^= y >> 27;
    y *= C6;
    uint64_t D = y ^ (y >> 31);

    return (uint16_t)(D ^ (D >> 16) ^ (D >> 32) ^ (D >> 48));
}

static int verify(uint64_t k0, uint64_t k1) {
    for (int i = 0; i < CONSTRAINTS; i++) {
        if (f33d0(HI[i], k0, k1) != TARGET[i])
            return 0;
    }
    return 1;
}

/* ---------- rank-62 map and its 2-dimensional kernel ---------- */
static uint64_t L(uint64_t x) {
    return x ^ rotl64(x, 46);
}

/* kernel basis of L (standard for this rotate distance) */
static const uint64_t KERNEL[4] = {
    0x0000000000000000ull,
    0x5555555555555555ull,
    0xaaaaaaaaaaaaaaaaull,
    0xffffffffffffffffull
};

/* ---------- global result ---------- */
static volatile int found = 0;
static uint64_t found_k0 = 0, found_k1 = 0;
static pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;

/* test the 4 kernel candidates around a base solution */
static int test_kernel(uint64_t base_k0, uint64_t base_k1) {
    for (int i = 0; i < 4; i++) {
        uint64_t k0 = base_k0 ^ KERNEL[i];
        uint64_t k1 = base_k1 ^ KERNEL[i];

        if (verify(k0, k1)) {
            pthread_mutex_lock(&lock);
            if (!found) {
                found = 1;
                found_k0 = k0;
                found_k1 = k1;
                printf("\n[+] KEY RECOVERED\n");
                printf("    k0 = 0x%016lx\n", k0);
                printf("    k1 = 0x%016lx\n", k1);
            }
            pthread_mutex_unlock(&lock);
            return 1;
        }
    }
    return 0;
}

/* ---------- worker ---------- */
typedef struct {
    uint32_t start, end;
    int id;
} job_t;

void *worker(void *arg) {
    job_t *job = (job_t *)arg;

    /*
     * Current search strategy (practical baseline):
     *   - enumerate 32 bits of k0
     *   - derive a candidate k1 from the linear first stage
     *     of the first constraint
     *   - test the 4-element kernel
     *
     * THIS IS WHERE THE REAL FOLD-LIFT BELONGS.
     * Replace the line that creates t2 with a value obtained by:
     *   1. lifting TARGET[0] through the final fold
     *   2. inverting the two splitmix stages
     *   3. obtaining a consistent (t2, t3) pair
     */
    for (uint32_t hi = job->start; hi < job->end && !found; hi++) {
        for (uint32_t lo = 0; lo < 0x10000u && !found; lo++) {
            uint64_t k0 = ((uint64_t)hi << 32) | lo;

            /* --- placeholder for the lifted t2 --- */
            uint64_t t_acc = (uint64_t)HI[0] * C1;
            uint64_t t2 = rotl64(k0, 13) ^ 0x9e3779b97f4a7c15ull; // <-- REPLACE THIS
            uint64_t k1 = rotl64(t2 ^ k0 ^ t_acc, 47);            // inv of rotl17

            if (test_kernel(k0, k1))
                return NULL;
        }
    }
    return NULL;
}

/* ---------- main ---------- */
int main(void) {
    printf("[*] SPI TPM key recovery\n");
    printf("[*] %d constraints, %d threads\n", CONSTRAINTS, NTHREADS);
    printf("[*] rank-62 map + 4-candidate kernel ready\n");
    printf("[*] fold-lift still placeholder – replace t2 generation\n\n");

    pthread_t threads[NTHREADS];
    job_t jobs[NTHREADS];
    uint32_t range = 0x100000000ull / NTHREADS;

    for (int i = 0; i < NTHREADS; i++) {
        jobs[i].start = i * range;
        jobs[i].end   = (i + 1) * range;
        jobs[i].id    = i;
        if (i == NTHREADS - 1) jobs[i].end = 0x100000000ull;
        pthread_create(&threads[i], NULL, worker, &jobs[i]);
    }

    for (int i = 0; i < NTHREADS; i++)
        pthread_join(threads[i], NULL);

    if (found) {
        printf("\n[+] SUCCESS\n");
        printf("k0 = 0x%016lx\n", found_k0);
        printf("k1 = 0x%016lx\n", found_k1);
        return 0;
    }

    printf("[-] No key found (expected – fold-lift still missing)\n");
    return 1;
}

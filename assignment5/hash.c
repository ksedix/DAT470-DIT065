#include <inttypes.h>
#include <stdint.h>
#include <stdlib.h>
#include <stdio.h>

uint64_t hash32u(uint64_t x, uint64_t l, uint64_t a) {
  return (a*x) >> (64-l);
}

uint32_t hash32su(uint32_t x, uint32_t l, uint64_t a, uint64_t b) {
  return (a*x+b) >> (64-l);
}

uint32_t hash32m(uint32_t x, uint32_t m, uint64_t a, uint64_t b) {
  return (((a*x+b)>>32)*m)>>32;
}

uint32_t hash64to32(uint64_t x, uint32_t l,
		    uint64_t a1, uint64_t a2, uint64_t b) {
  return ((a1+x)*(a2+(x>>32))+b) >> (64-l);
}

uint64_t hash64to64(uint64_t x, uint64_t l, uint64_t a1, uint64_t a2,
		    uint64_t a3, uint64_t a4, uint64_t b1, uint64_t b2) {
  uint64_t y = hash64to32(x, 32, a1, a2, b1);
  y <<= 32;
  y |= hash64to32(x, 32, a3, a4, b2);
  return y >> (64-l);
}

static uint64_t random64(void) {
  uint64_t x = arc4random();
  x <<= 32;
  x |= arc4random();
  return x;
}

int main(void) {
  uint64_t a1, a2, a3, a4, b1, b2, x, h;
  a1 = random64();
  a2 = random64();
  a3 = random64();
  a4 = random64();
  b1 = random64();
  b2 = random64();
  x = random64();
  h = hash64to64(x,64,a1,a2,a3,a4,b1,b2);
  printf("a1=%016" PRIx64 "\n",a1);
  printf("a2=%016" PRIx64 "\n",a2);
  printf("a3=%016" PRIx64 "\n",a3);
  printf("a4=%016" PRIx64 "\n",a4);
  printf("b1=%016" PRIx64 "\n",b1);
  printf("b2=%016" PRIx64 "\n",b2);
  printf("x=%016" PRIx64 "\n",x);
  printf("h=%016" PRIx64 "\n",h);

  return 0;
}

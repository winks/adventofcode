#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

enum Type {None = 0, Cut = 1, DealNew = 2, DealInc = 4};

struct Step {
	enum Type type;
	__int64_t num;
};

void pps(struct Step s) {
	if (s.type == 0) printf("None\n");
	if (s.type == 1) printf("Cut %ld\n", s.num);
	if (s.type == 2) printf("Deal New\n");
	if (s.type == 4) printf("Deal Inc %ld\n", s.num);
}

void ppd(int **orig_deck, size_t deck_size) {
	printf("TOP [");
	for (size_t i=0; i<deck_size; ++i) {
		printf(" %d", (*orig_deck)[i]);
	}
	printf(" ] BOT\n");
}

int parse(char *line, struct Step *rv) {
	rv->type = None;
	rv->num = 0;
	char *xcut = "cut ";
	char *xdealnew = "deal into";
	char *xdealinc = "deal with increment ";
	char *ptr;

	ptr = strstr(line, xcut);
	if (ptr != NULL) {
		ptr += strlen(xcut);
		char *end;
		rv->num = strtoll(ptr, &end, 10);
		if (*end) return 11;
		rv->type = Cut;
		pps(*rv);

		return 0;
	}
	ptr = strstr(line, xdealnew);
	if (ptr != NULL) {
		rv->type = DealNew;
		pps(*rv);

		return 0;
	}
	ptr = strstr(line, xdealinc);
	if (ptr != NULL) {
		ptr += strlen(xdealinc);
		char *end;
		rv->num = strtoll(ptr, &end, 10);
		if (*end) return 12;
		rv->type = DealInc;
		pps(*rv);

		return 0;
	}
	return 15;
}

void part1(int **deck, size_t len) {
	if (len < 2000) return;
	size_t x = 1;
	for (size_t i=(len-1); i!=0; --i) {
		//printf(" %ld> %d\n", i, (*deck)[i]);
		if ((*deck)[i] == 2019) {
			printf("FOUND %ld : %d => %ld\n", i, (*deck)[i], x);
			return;
		}
		++x;
	}
}

void shuffle(int **orig_deck, size_t deck_size, struct Step steps[], size_t num_steps) {
	int deck[deck_size];
	for (size_t i=0; i<deck_size; ++i) {
		deck[i] = 0;
	}
	printf("Deck : %ld\n", deck_size);
	printf("Steps: %ld\n", num_steps);
	ppd(orig_deck, deck_size);

	for (size_t i=0; i<num_steps; ++i) {
		if (steps[i].type < 1) continue;
		if (steps[i].type > 4) continue;
		printf("Current step: ");
		pps(steps[i]);

		if (steps[i].type == DealNew) {
			for (size_t i=0; i<deck_size; ++i) {
				deck[deck_size - 1 - i] = (*orig_deck)[i];
			}
		}
		if (steps[i].type == Cut) {
			__int64_t n = steps[i].num;
			if (n > 0) {
				for (int i=0;i<n;++i) {
					deck[deck_size - n + i] = (*orig_deck)[i];
				}
				for (int i=n;i<deck_size;++i) {
					deck[0 - n + i] = (*orig_deck)[i];
				}
			} else {
				for (int i=(deck_size+n);i<deck_size;++i) {
					deck[i - (deck_size+n)] = (*orig_deck)[i];
				}
				for (int i=0;i<(deck_size+n);++i) {
					deck[0 - n + i] = (*orig_deck)[i];
				}

			}
		}
		if (steps[i].type == DealInc) {
			__int64_t n = steps[i].num;
			size_t pos = 0;
			deck[0] = (*orig_deck)[0];
			for (int i=1;i<deck_size;++i) {
				pos = (pos + n);
				deck[pos % deck_size] = (*orig_deck)[i];
			}
		}
		for (size_t i=0; i<deck_size; ++i) {
			(*orig_deck)[i] = deck[i];
		}
		ppd(orig_deck, deck_size);
	}
	part1(orig_deck, deck_size);
}

__int128 mod_exp(__int128 base, __int128 exponent, __int128 modulus) {
	__int128 result = 1;
	base = base % modulus;

	while (1) {
		if (exponent <= 0) {
			break;
		}
		if (exponent % 2 == 1) {
			result = (result * base) % modulus;
		}
		exponent = exponent >> 1;
		base = (base * base) & modulus;
	}
	return result;
}

void shuffle2(struct Step steps[], size_t num_steps) {
	__int128 pos = 2020;
	__int128 len = 119315717514047;
	__int128 times = 101741582076661;
	__int128 off = 0;
	__int128 inc = 1;

	for (size_t i=0; i<num_steps; ++i) {
		if (steps[i].type < 1) continue;
		if (steps[i].type > 4) continue;
		printf("Current step: ");
		pps(steps[i]);

		if (steps[i].type == DealNew) {
			off = off - inc;
			inc = -inc;
		}
		if (steps[i].type == Cut) {
			off = off + inc * steps[i].num;
		}
		if (steps[i].type == DealInc) {
			inc = inc * mod_exp(steps[i].num, len - 2, len);
		}
		off = off % len;
		inc = inc % len;
	}
	__int128 incr = mod_exp(inc, times, len);
	__int128 offs = off * (1 - mod_exp(inc, times, len)) % len;
	offs = offs * mod_exp(1 - inc, len - 2, len) % len;
	__int128 r = (offs + incr * pos) % len;

	printf("Part 2: %ld :: %ld\n", off, inc);
	printf("Part 2: %ld :: %ld\n", offs, incr);
	printf("Part 2: %ld :: %ld\n", pos, r);
}

const __int64_t mm = 119315717514047;
const __int64_t nn = 101741582076661;

__int64_t add(__int64_t a, __int64_t b) {
	return (mm + (a + b) % mm) % mm;
}

__int64_t mul(__int64_t a, __int64_t b) {
	__int64_t unit = 0;
	for (__int64_t r = unit;; b >>= 1, a = add(a, a)) {
		if (!b) return r;
		if (b & 1) r = add(r, a);
	}
}

__int64_t powx(__int64_t a, __int64_t b) {
	__int64_t unit = 1;
	for (__int64_t r = unit;; b >>= 1, a = mul(a, a)) {
		if (!b) return r;
		if (b & 1) r = mul(r, a);
	}
}

void shuffle3(struct Step steps[], size_t num_steps) {
	__int64_t pos = 2020;
	__int64_t off = 0;
	__int64_t inc = 1;
	__int64_t k = 1;
	__int64_t b = 0;
	__int64_t x;

	for (size_t i=0; i<num_steps; ++i) {
		if (steps[i].type < 1) continue;
		if (steps[i].type > 4) continue;
		printf("Current step: ");
		pps(steps[i]);

		if (steps[i].type == DealNew) {
			k = add (0, -k);
			b = add(-1, -b);
		}
		if (steps[i].type == Cut) {
			b = add(b, -steps[i].num);
		}
		if (steps[i].type == DealInc) {
			x = steps[i].num;
			k = mul(k, x);
			b = mul(b, x);
		}
	}
	x = mul(b, powx(k - 1, mm - 2));
	x = add(mul(add(x, pos), powx( powx(k, mm - 2), nn)), -x);
	printf("Part 2: %ld :: %ld\n", pos, x);
}

int main(int argc, char *argv[]) {
	if (argc < 3) {
		printf("Usage: %s /path/to/file decksize [2]\n", argv[0]);
		return 1;
	}
	char *filename = argv[1];

	char *ds = argv[2];
	__int64_t decksize = 0;
	char *ds_end;
	decksize = strtoll(ds, &ds_end, 10);
	if (*ds_end) return 2;
	if (decksize < 10) decksize = 10;
	printf("deck size: %ld\n", decksize);
	__int64_t part = 1;
	if (argc > 3) {
		char *part2s = argv[3];
		char *p_end;
		part = strtoll(part2s, &p_end, 10);
	}

	FILE *fp;
	char *line = NULL;
	size_t len = 0;
	ssize_t read;
	fp = fopen(filename, "r");
	if (fp == NULL) return 3;

	size_t num_steps = 101;
	struct Step steps[num_steps];
	size_t idx = 0;

	while ((read = getline(&line, &len, fp)) != -1) {
		line[strcspn(line, "\n")] = 0;
		printf("# %ld>%s<\n", idx, line);
		struct Step stp;
		parse(line, &stp);
		steps[idx] = stp;
		++idx;
	}
	fclose(fp);
	struct Step dummy;
	dummy.type = None;
	for (size_t i=idx; i<num_steps; ++i) {
		steps[i] = dummy;
	}

	int *deck;
	deck = malloc(decksize * sizeof(int));
	for (size_t i=0; i<decksize; ++i) {
		deck[i] = i;
	}

	ppd(&deck, decksize);
	if (part == 2) shuffle3(steps, num_steps);
	else shuffle(&deck, decksize, steps, num_steps);
}

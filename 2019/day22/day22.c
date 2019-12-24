#include <stdio.h>
#include <stdlib.h>
#include <string.h>

enum Type {None = 0, Cut = 1, DealNew = 2, DealInc = 4};

struct Step {
	enum Type type;
	__int64_t num;
};

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
		printf("# CUT:%s:%ld\n", ptr, rv->num);

		return 0;
	}
	ptr = strstr(line, xdealnew);
	if (ptr != NULL) {
		rv->type = DealNew;
		printf("# DEAL NEW\n");

		return 0;
	}
	ptr = strstr(line, xdealinc);
	if (ptr != NULL) {
		ptr += strlen(xdealinc);
		char *end;
		rv->num = strtoll(ptr, &end, 10);
		if (*end) return 12;
		rv->type = DealInc;
		printf("# DEAL INC:%s:%ld\n", ptr, rv->num);

		return 0;
	}
	return 15;
}

void part1(int deck[], size_t len) {
	size_t x = 1;
	for (size_t i=(len-1); i!=0; --i) {
		printf(" %ld> %d\n", i, deck[i]);
		if (deck[i] == 2019) {
			printf("FOUND %ld : %d => %ld\n", i, deck[i], x);
			return;
		}
		++x;
	}
}

int main(int argc, char *argv[]) {
	if (argc < 3) {
		printf("Usage: %s /path/to/file decksize \n", argv[0]);
		return 1;
	}
	char *filename = argv[1];

	char *ds = argv[2];
	__int64_t decksize = 0;
	char *ds_end;
	decksize = strtoll(ds, &ds_end, 10);
	if (*ds_end) return 2;
	printf("deck size: %ld\n", decksize);

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

	int deck[decksize];
	for (size_t i=0; i<decksize; ++i) {
		deck[i] = i;
	}

	part1(deck, decksize);

	//for (int i=0; i<num_steps; ++i) {
	//	if (steps[i].type != None) printf("%d %d %ld\n", i, steps[i].type, steps[i].num);
	//	else printf("%d 000\n", i);
	//}
}

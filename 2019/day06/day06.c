#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int isleaf(char * k, char rv[1000][4]) {
	for (size_t i=0;i<1000;++i) {
		if (strlen(rv[i]) < 1) continue;
		if (strcmp(rv[i], k) == 0) return 0;
	}
	return 1;
}

int main(int argc, char * argv[]){
	if (argc < 2) {
		printf("Usage: %s /path/to/file\n", argv[0]);
		return 1;
	}
	char *filename = argv[1];

	FILE *fp;
	char *line = NULL;
	size_t llen = 0;
	ssize_t read;
	fp = fopen(filename, "r");
	if (fp == NULL)return 3;

	int nlines = 1000;
	//char data[nlines][8];
	char fkeys[nlines][4];
	char fvals[nlines][4];
	char rkeys[nlines][4];
	char rvals[nlines][4];

	// read all lines, split at ")"
	// put second part into rkeys
	// put first part into rvals, with the same index
	size_t idx = 0;
	size_t len = 0;
	while ((read = getline(&line, &llen, fp)) != -1) {
		line[strcspn(line, "\n")] = 0;
		char * p2 = strstr(line, ")");
		if (!p2) {
			printf("ERROR %s\n", line);
			continue;
		}
		int pos = p2 - line;
		char * key = p2+1;
		strncpy(fkeys[idx], line, pos);
		strncpy(fvals[idx], key, 3);
		int found = -1;
		if (len > 0) {
			for (size_t i=0;i<len;++i) {
				if (rkeys[i] == key) {
					found = i;
					break;
				}
			}
		}
		if (len == 0 || found < 0) {
			strncpy(rvals[idx], line, pos);
			strncpy(rkeys[idx], key, strlen(key));
			len++;
		}
		++idx;
	}
	fclose(fp);

	int total = 0;
	char done[nlines][4];
	for (size_t i=0;i<nlines;++i) {
		strncpy(done[i], "\0\0\0\0", 4);
	}
	size_t donelen = 0;
	char psan[nlines][4];
	char pyou[nlines][4];
	int lyou = 0;
	int lsan = 0;
	// check all rkeys, only look at leaves
	for (size_t i=0;i<len;++i) {
		if (strlen(rkeys[i]) < 1) continue;
		if (!isleaf(rkeys[i], rvals)) continue;
		char *end = "COM";

		char rv[nlines][4];
		size_t pos = 0;
		char cur[4];
		strncpy(cur, "\0\0\0\0\0", 4);
		strncpy(cur, rkeys[i], strlen(rkeys[i]));
		while (strcmp(end, cur) != 0) {
			for (size_t ii=0;ii<1000;++ii) {
				if (strlen(rkeys[ii]) < 1) continue;
				if (strcmp(rkeys[ii], cur) == 0) {
					strncpy(rv[pos], "\0\0\0\0\0", 4);
					strncpy(rv[pos], cur, strlen(cur));
					strncpy(cur, "\0\0\0\0\0", 4);
					strncpy(cur, rvals[ii], strlen(rvals[ii]));
					++pos;
					break;
				}
			}
		}
		strncpy(rv[pos], "COM\0",4);
		strncpy(rv[++pos], "\0\0\0\0",4);
		for (int ii=pos-1;ii>=0;--ii) {
			if (strlen(rv[ii]) < 1) continue;
			if (donelen == 0) {
				strncpy(done[donelen], "\0\0\0\0", 4);
				strncpy(done[donelen], rv[ii], strlen(rv[ii]));
				++donelen;
			}
			int found = 0;
			for (size_t jj=0;jj<donelen;++jj){
				if (strcmp(rv[ii], done[jj]) == 0) {
					found = 1;
					break;
				}
			}
			if (found == 0) {
				strncpy(done[donelen], "\0\0\0\0", 4);
				strncpy(done[donelen], rv[ii], strlen(rv[ii]));
				total += (pos-ii-1);
				++donelen;
			}
		}
		// part 2 starts here
		if (strcmp(rv[0], "YOU") == 0) {
			//printf("YOU: %ld\n", pos);
			lyou = pos-1;
			for (int ii=lyou;ii>=0;--ii) {
				strncpy(pyou[lyou-ii], "\0\0\0\0", 4);
				strncpy(pyou[lyou-ii], rv[ii], strlen(rv[ii]));
			}
		}
		if (strcmp(rv[0], "SAN") == 0) {
			//printf("SAN: %ld %s\n", pos, rv[pos-1]);
			lsan = pos-1;
			for (int ii=lsan;ii>=0;--ii) {
				strncpy(psan[lsan-ii], "\0\0\0\0", 4);
				strncpy(psan[lsan-ii], rv[ii], strlen(rv[ii]));
			}
		}
	}
	printf("Part 1: %d\n", total);
	//printf("Y: %s %s\n", pyou[0], pyou[lyou-1]);
	//printf("S: %s %s\n", psan[0], psan[lsan-1]);

	for (int i=0;i<lyou;++i) {
		if (strcmp(pyou[i], psan[i]) == 0) {
			//printf("SAME: %s %d\n", pyou[i], i);
			continue;
		}
		//printf("DIFF: %s %s %d\n", pyou[i], psan[i], i);
		printf("Part 2: %d\n", (lyou+lsan-i-i));
		break;
	}
}

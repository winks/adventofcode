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

int walk(char * start, char rkeys[1000][4], char rvals[1000][4], char **rv) {
	int pos = 0;
	char *end = "COM";
	char cur[4];
	printf("WW >%s<>%s<\n", start, end);
	strncpy(cur, start, 4);
	printf("WW >%s<>%s<>%s<\n", start, cur, rv[pos]);
	while (strcmp(end, cur) != 0) {
		for (size_t i=0;i<1000;++i) {
			if (strlen(rkeys[i]) < 1) continue;
			if (strcmp(rkeys[i], cur) == 0) {
				//strncpy(rv[pos], cur, strlen(cur));
				rv[pos] = strdup(cur);
				//strncpy((*rv)[pos], cur, strlen(cur));
				++pos;
				break;
			}
		}
	}
	return 0;
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
	char keys[nlines][4];
	char vals[nlines][4];
	char rkeys[nlines][4];
	char rvals[nlines][4];

	size_t idx = 0;
	size_t len = 0;
	while ((read = getline(&line, &llen, fp)) != -1) {
		line[strcspn(line, "\n")] = 0;
		//printf("# %ld>%s<\n", idx, line);
		char * p2 = strstr(line, ")");
		if (!p2) {
			printf("ERROR %s\n", line);
			continue;
		}
		int pos = p2 - line;
		char * key = p2+1;
		//printf("K >%s< len: %ld\n", key, len);
		//strncpy(data[idx], line, 7);
		strncpy(keys[idx], line, pos);
		strncpy(vals[idx], key, 3);
		int found = -1;
		if (len > 0) {
			for (size_t i=0;i<len;++i) {
				//printf("FF %s ~ %s < len: %ld\n", rkeys[i], key, i);
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
		//steps[idx] = stp;
		++idx;
		//printf("\n");
	}
	fclose(fp);

	//printf("IDX   %ld\n", idx);
	//printf("LEN   %ld\n", len);
	//printf("DATA  %s %ld\n", data[0], strlen(data[0]));
	for (size_t i=0;i<len;++i) {
		if (strlen(rkeys[i]) < 1) continue;
		//printf("RKEY  %s\t%ld", rkeys[i], strlen(rkeys[i]));
		//printf("\t%s\t%ld\tRVALS\n", rvals[i], strlen(rvals[i]));
	}
	//printf("KEYS  %s %ld\n", keys[0], strlen(keys[0]));
	//printf("VALS  %s %ld\n", vals[0], strlen(vals[0]));
	//printf("DATA  %s %ld\n", data[len-1], strlen(data[len-1]));
	//printf("RKEYS %s %ld\n", rkeys[len-1], strlen(rkeys[len-1]));
	//printf("RVALS %s %ld\n", rvals[len-1], strlen(rvals[len-1]));
	//printf("\n");
	//printf("%d \n", isleaf("L", rvals));
	//printf("%d \n", isleaf("B", rvals));
	//printf("%d \n", isleaf("COM",rvals));
	//printf("%d \n", isleaf("H",rvals));
	//printf("%d \n", isleaf("C",rvals));
	//printf("\n");
	int total = 0;
	////size_t pathlen[nlines];
	char done[nlines][4];
	for (size_t i=0;i<nlines;++i) {
		strncpy(done[i], "\0\0\0\0", 4);
	}
	size_t donelen = 0;
	// sortit
	for (size_t i=0;i<len;++i) {
		if (strlen(rkeys[i]) < 1) continue;
		if (!isleaf(rkeys[i], rvals)) continue;
		//printf("L >%s<\n", rkeys[i]);
		//int x = walk(rkeys[i], rkeys, rvals, &rv);
		char *end = "COM";

		char rv[nlines][4];
		size_t pos = 0;
		char cur[4];
		//printf("WW >%s<>%s<\n", start, end);
		strncpy(cur, "\0\0\0\0\0", 4);
		strncpy(cur, rkeys[i], strlen(rkeys[i]));
		//printf("WW1 >%ld<>%s<>%s<\n", pos, cur, rv[pos]);
		while (strcmp(end, cur) != 0) {
			//printf("WW2 >%ld<>%s<>%s<\n", pos, cur, rv[pos]);
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
		//for (size_t ii=0;ii<pos;++ii) {
		//	if (strlen(rv[ii]) < 1) continue;
		//	printf("%s ", rv[ii]);
		//}
		//printf("| POS %ld \n", pos);
		for (int ii=pos-1;ii>=0;--ii) {
			//printf("  NOW %s \n", rv[ii]);
			if (strlen(rv[ii]) < 1) continue;
			if (donelen == 0) {
				strncpy(done[donelen], "\0\0\0\0", 4);
				strncpy(done[donelen], rv[ii], strlen(rv[ii]));
				//printf(" DD %ld %d >%s< >%s<\n", donelen, 0, rv[ii], done[0]);
				++donelen;
			}
			int found = 0;
			for (size_t jj=0;jj<donelen;++jj){
				//printf("  DL %ld/%ld >%s< >%s<\n", jj,donelen, rv[ii], done[jj]);
				if (strcmp(rv[ii], done[jj]) == 0) {
					found = 1;
					break;
				}
				//printf("  DL %ld/%ld >%s< >%s<\n", jj,donelen, rv[ii], done[jj]);
			}
			if (found == 0) {
				strncpy(done[donelen], "\0\0\0\0", 4);
				strncpy(done[donelen], rv[ii], strlen(rv[ii]));
				//printf("   DD %ld %d >%s< >%s< %d\n", donelen, found, rv[ii], done[donelen], ii);
				//printf("%ld pts for >%s<\n", (pos-ii-1), rv[ii]);
				total += (pos-ii-1);
				++donelen;
			}
			//printf("\n");
			//for (size_t jj=0;jj<donelen;++jj){
			//	printf(" DONE %ld %s\n", jj, done[jj]);
			//}
			//printf("\n");
			//printf("\n");
		}
		//printf("| POS %ld \n", pos);
	}
	printf("Part 1: %d\n", total);
}

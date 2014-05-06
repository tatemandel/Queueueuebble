#pragma once

typedef struct amember {
  char username[20];
  int id;
  int pos;
  int status;
} amember;

void aqueue_init(void);
void aqueue_deinit(void);
void aqueue_show(int id);
void aqueue_add(char*, int, int, int);
void aqueue_reset();
int get_aid();
void set_aid(int);
Layer* getAQueueWindowLayer();

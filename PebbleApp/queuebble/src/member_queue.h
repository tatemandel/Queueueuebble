#pragma once

typedef struct mmember {
  char username[20];
  int id;
  int pos;
  int status;
} mmember;

void mqueue_init(void);
void mqueue_deinit(void);
void mqueue_show(int id);
void mqueue_add(char*, int, int, int);
void mqueue_reset();
int get_mid();
Layer* getMQueueWindowLayer();

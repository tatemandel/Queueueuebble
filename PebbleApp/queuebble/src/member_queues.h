#pragma once
#include <pebble.h>

void mqueues_init(void);
void mqueues_deinit(void);
void mqueues_show(void);
void mqueues_add(char*, char*, int, int, int);
void mqueues_reset();
Layer* getMemberWindowLayer();
void mqueues_clean(int);

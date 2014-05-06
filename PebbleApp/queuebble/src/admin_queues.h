#pragma once
#include <pebble.h>

void aqueues_init(void);
void aqueues_deinit(void);
void aqueues_show(void);
void aqueues_add(int, int, char*, int);
void aqueues_reset();
Layer* getAdminWindowLayer();

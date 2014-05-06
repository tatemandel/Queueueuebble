#pragma once

void home_init(void);
void home_deinit(void);
void send_messages(char*);
void load_queue(int, char*);
char* get_username();
void update_status(char*, int, int);

#include <pebble.h>
#include "home.h"
#include "admin_queue.h"
#include "member_queue.h"
#include "admin_queues.h"
#include "member_queues.h"

#define NUM_MENU_ITEMS 2
#define NUM_MENU_SECTIONS 1
#define TIME_INTERVAL 10000
#define USERNAME_KEY 1

static Window *window;

static Layer *window_layer;
static MenuLayer *menu_layer;
static TextLayer *text_layer;
static AppTimer *timer;

static char username[50];

int received = 0;
int whichUpdate = 0;

enum {
  BLANK, // 0
  USER_KEY, // 1
  ID_KEY, // 2
  NAME_KEY, // 3
  SIZE_KEY, // 4
  STATUS_KEY, // 5
  NUM_KEY, // 6
  CREATOR_KEY, // 7
  POSITION_KEY, // 8
  TYPE_KEY, // 9
  NO_DATA_KEY, // 10
  SHOW_KEY, //11
  UPDATE_KEY, // 12
};

void out_sent_handler(DictionaryIterator *sent, void *context) {
  APP_LOG(APP_LOG_LEVEL_DEBUG, "Sent");
}

void out_failed_handler(DictionaryIterator *failed, AppMessageResult reason, void *context) {
  APP_LOG(APP_LOG_LEVEL_DEBUG, "App Message Failed to Send!");
}

void in_dropped_handler(AppMessageResult reason, void *context) {
  APP_LOG(APP_LOG_LEVEL_DEBUG, "App Message Dropped!");
}

static void in_received_handler(DictionaryIterator *iter, void *context) {
  Tuple *user_t = dict_find(iter, USER_KEY);
  Tuple *id_t = dict_find(iter, ID_KEY);
  Tuple *name_t = dict_find(iter, NAME_KEY);
  Tuple *size_t = dict_find(iter, SIZE_KEY);
  Tuple *status_t = dict_find(iter, STATUS_KEY);
  Tuple *num_t = dict_find(iter, NUM_KEY);
  Tuple *creator_t = dict_find(iter, CREATOR_KEY);
  Tuple *pos_t = dict_find(iter, POSITION_KEY);
  Tuple *type_t = dict_find(iter, TYPE_KEY);
  Tuple *no_data_t = dict_find(iter, NO_DATA_KEY);
  Tuple *show_t = dict_find(iter, SHOW_KEY);
  Tuple *update_t = dict_find(iter, UPDATE_KEY);

  if (id_t && name_t && size_t && status_t && num_t && update_t) {
    APP_LOG(APP_LOG_LEVEL_DEBUG, "received one admin");
    received++;
    char name[50];
    strcpy(name, name_t->value->cstring);
    int id = id_t->value->int32;
    int size = size_t->value->int32;
    int status = status_t->value->int32;
    int num = num_t->value->int32;
    int update = update_t->value->int32;
    aqueues_add(size, id, name, status);
    if (received == num) {
      received = 0;
      //      layer_remove_from_parent(text_layer_get_layer(text_layer));
      //      layer_add_child(window_layer, menu_layer_get_layer(menu_layer));  
      if (update == 0) {
	aqueues_show();
      }
      else if (update == 1) {
	layer_mark_dirty(getAdminWindowLayer());
      }
    }
  }
  else if (id_t && name_t && status_t && num_t && creator_t && pos_t && update_t) {
    APP_LOG(APP_LOG_LEVEL_DEBUG, "received one member");
    received++;
    char name[50];
    strcpy(name, name_t->value->cstring);
    char creator[50];
    strcpy(creator, creator_t->value->cstring);
    int id = id_t->value->int32;
    int status = status_t->value->uint8;
    int num = num_t->value->int32;
    int pos = pos_t->value->int32;
    int update = update_t->value->int32;
    mqueues_add(name, creator, pos, id, status);
    if (received == num) {
      received = 0;
      //      layer_remove_from_parent(text_layer_get_layer(text_layer));
      //      layer_add_child(window_layer, menu_layer_get_layer(menu_layer));
      if (update == 0) {
        APP_LOG(APP_LOG_LEVEL_DEBUG, "update is 0");
	mqueues_show();
      }
      else if (update == 1) {
        APP_LOG(APP_LOG_LEVEL_DEBUG, "update is 1");
	layer_mark_dirty(getMemberWindowLayer());
      }
    }
  } else if (user_t && id_t && status_t && num_t && pos_t && type_t && update_t) { // users added
    received++;
    char user[50];
    strcpy(user, user_t->value->cstring);
    int id = id_t->value->int32;
    int status = status_t->value->int32;
    int num = num_t->value->int32;
    int pos = pos_t->value->int32;
    int type = type_t->value->int32;
    int update = update_t->value->int32;

    if (type == 1) {
      APP_LOG(APP_LOG_LEVEL_DEBUG, "adding a user");
      aqueue_add(user, id, pos, status);
    } else if (type == 2) {
      APP_LOG(APP_LOG_LEVEL_DEBUG, "mqueue add");
      mqueue_add(user, id, pos, status);
    }
    if (received == num) {
      received = 0;
      if (type == 1) {
        if (show_t == NULL && update == 0) {
          aqueue_show(id);
        } else if (show_t) { // changed something about queues. Make sure previous page is still correct
          aqueues_clean(id, num);
        } else if (update == 1) {
	  layer_mark_dirty(getAQueueWindowLayer());
        }
      } else if (type == 2) {
        if (show_t == NULL && update == 0) {
	  mqueue_show(id);
        } else if (show_t) {
          mqueues_clean(id);
          APP_LOG(APP_LOG_LEVEL_DEBUG, "cleaning members");
          // clean the member page to not have the queue anymore
        } else if (update == 1) {
	  layer_mark_dirty(getMQueueWindowLayer());
        }
      }
    }
  } else if (no_data_t && type_t && update_t) {
    if (no_data_t->value->int32 == 3 && type_t->value->int32 == 1) {
      if (update_t->value->int32 == 0) {
	  aqueue_show(-1);
      }
      else if (update_t->value->int32 == 1) {
	layer_mark_dirty(getAQueueWindowLayer());
      }
    }
    else if (no_data_t->value->int32 == 3 && type_t->value->int32 == 2) {
      if (update_t->value->int32 == 0) {
	  mqueue_show(-1);
      }
      else if (update_t->value->int32 == 1) {
	layer_mark_dirty(getMQueueWindowLayer());
      }
    }
  } else if (no_data_t && update_t) {
    if (update_t->value->int32 == 0) {
      layer_remove_from_parent(text_layer_get_layer(text_layer));
      layer_add_child(window_layer, menu_layer_get_layer(menu_layer));
      if (no_data_t->value->int32 == 1) { 
        aqueues_show();
      }
      else if (no_data_t->value->int32 == 2) {
        mqueues_show();
      } 
    }
  } else if (user_t) {
    strcpy(username, user_t->value->cstring);
    layer_remove_from_parent(text_layer_get_layer(text_layer));
    menu_layer_set_click_config_onto_window(menu_layer, window);
    layer_add_child(window_layer, menu_layer_get_layer(menu_layer));
  }
}

static void menu_draw_row_callback(GContext* ctx, const Layer *cell_layer, 
				   MenuIndex *cell_index, void *data) {
  switch (cell_index->row) {
  case 0:
    menu_cell_basic_draw(ctx, cell_layer, "Owner", NULL, NULL);
    break;
  case 1:
    menu_cell_basic_draw(ctx, cell_layer, "Member", NULL, NULL);
    break;
  }
}

static uint16_t menu_get_num_rows_callback(MenuLayer *menu_layer, 
					   uint16_t section_index, void *data) {
  switch (section_index) {
  case 0:
    return NUM_MENU_ITEMS;
  default:
    return 0;
  }
}

// Here we draw what each header is                                    
static void menu_draw_header_callback(GContext* ctx, const Layer *cell_layer, uint16_t section_index, void *data) {
  // Determine which section we're working with 
  switch (section_index) {
  case 0:
    // Draw title text in the section header
    menu_cell_basic_header_draw(ctx, cell_layer, "Options");
    break;
  }
}

static uint16_t menu_get_num_sections_callback(MenuLayer *menu_layer, void *data) {
  return NUM_MENU_SECTIONS;
}

// A callback is use id to specify the height of the section header
static int16_t menu_get_header_height_callback(MenuLayer *menu_layer, uint16_t section_index, void *data) {
  // This is a define provided in pebble.h that you may use for the default height                                                             
  return MENU_CELL_BASIC_HEADER_HEIGHT;
}

void update_status(char *uname, int id, int status) {
  char *type = status == 0 ? "nstart" : status == 1 ? "progress" : 
               status == 2 ? "aremove" : status == 3 ? "up" : 
               status == 4 ? "down" : status == 5 ? "mremove" : "favorite";
  if (status == 2 || status == 3 || status == 4) {
    aqueue_reset();
  }
  if (status == 5) {
    mqueue_reset();
  }
  DictionaryIterator *iter;
  app_message_outbox_begin(&iter);
  dict_write_cstring(iter, 1, type);
  Tuplet value = TupletInteger(2, id);
  dict_write_tuplet(iter, &value);
  dict_write_cstring(iter, 3, uname);
  dict_write_end(iter);
  app_message_outbox_send();
}

void load_queue(int id, char *type) {
  //  text_layer_set_text(text_layer, "Loading...");
  //  layer_add_child(window_layer, text_layer_get_layer(text_layer));
  DictionaryIterator *iter;
  app_message_outbox_begin(&iter);
  dict_write_cstring(iter, 1, type);
  Tuplet value = TupletInteger(2, id);
  dict_write_tuplet(iter, &value);
  dict_write_end(iter);
  app_message_outbox_send();
}

void send_messages(char *type) {
  //  layer_remove_from_parent(menu_layer_get_layer(menu_layer));
  //  text_layer_set_text(text_layer, "Loading...");
  //  layer_add_child(window_layer, text_layer_get_layer(text_layer));  
  DictionaryIterator *iter;
  app_message_outbox_begin(&iter);
  dict_write_cstring(iter, 1, type);
  dict_write_cstring(iter, 2, username);
  dict_write_end(iter);
  app_message_outbox_send();
}

static void timer_callback(void *data) {
  APP_LOG(APP_LOG_LEVEL_DEBUG, "tick");
  if (whichUpdate == 0) {
    whichUpdate = 1;
    mqueues_reset();
    send_messages("memberUpdate");
  }
  else if (whichUpdate == 1) {
    whichUpdate = 2;
    aqueues_reset();
    send_messages("adminUpdate");
  }
  else if (whichUpdate == 2) {
    whichUpdate = 3;
    aqueue_reset();
    int a = get_aid();
    if (a > 0) load_queue(a, "aqueueUpdate");
  }
  else if (whichUpdate == 3) {
    whichUpdate = 0;
    aqueue_reset();
    int m = get_mid();
    if (m > 0) load_queue(m, "mqueueUpdate");
  }
  timer = app_timer_register(TIME_INTERVAL, timer_callback, NULL);
}

void menu_select_callback(MenuLayer *menu_layer, MenuIndex *cell_index, 
			  void *data) {
  switch (cell_index->row) {
  case 0:
    aqueues_reset();
    send_messages("admin");
    break;
  case 1:
    mqueues_reset();
    send_messages("member");
    break;
  }
}

static void window_load(Window *window) {
  window_layer = window_get_root_layer(window);
  GRect bounds = layer_get_frame(window_layer);

  menu_layer = menu_layer_create(bounds);

  menu_layer_set_callbacks(menu_layer, NULL, (MenuLayerCallbacks) {
    .get_num_sections = menu_get_num_sections_callback,
    .get_num_rows = menu_get_num_rows_callback,
    .get_header_height = menu_get_header_height_callback,
    .draw_header = menu_draw_header_callback,
    .draw_row = menu_draw_row_callback,
    .select_click = menu_select_callback, 
  });

  text_layer = text_layer_create((GRect) { .origin = { 0, 72 }, .size = { bounds.size.w, 20 } });
  text_layer_set_text(text_layer, "Login to Queuebble");
  text_layer_set_text_alignment(text_layer, GTextAlignmentCenter);

  if (username[0] == '\0') {
    layer_add_child(window_layer, text_layer_get_layer(text_layer));
  } else {
    menu_layer_set_click_config_onto_window(menu_layer, window);
    layer_add_child(window_layer, menu_layer_get_layer(menu_layer));
  }

  timer = app_timer_register(TIME_INTERVAL, timer_callback, NULL);
}

static void window_unload(Window *window) {
  persist_write_string(USERNAME_KEY, username);
  menu_layer_destroy(menu_layer);
}

void home_init(void) {
  window = window_create();
  window_set_window_handlers(window, (WindowHandlers) {
    .load = window_load,
    .unload = window_unload,
  });

  username[0] = '\0';
  if (persist_exists(USERNAME_KEY)) persist_read_string(USERNAME_KEY, username, 50);

  app_message_register_inbox_received(in_received_handler);
  app_message_open(512, 512);

  const bool animated = true;
  window_stack_push(window, animated);
}

void home_deinit(void) {
  window_destroy(window);
}

char* get_username() {
  return username;
}

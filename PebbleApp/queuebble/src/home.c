#include <pebble.h>
#include "home.h"
#include "admin_queues.h"
#include "member_queues.h"

#define NUM_MENU_ITEMS 2
#define NUM_MENU_SECTIONS 1

#define USERNAME_KEY 1

static Window *window;

static Layer *window_layer;
static MenuLayer *menu_layer;
static TextLayer *text_layer;

static char username[50];

enum {
  BLANK,
  USER_KEY,
};

static void in_received_handler(DictionaryIterator *iter, void *context) {
  Tuple *t = dict_find(iter, USER_KEY);

  if (t) {
    strcpy(username, t->value->cstring);
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

// A callback is used to specify the height of the section header
static int16_t menu_get_header_height_callback(MenuLayer *menu_layer, uint16_t section_index, void *data) {
  // This is a define provided in pebble.h that you may use for the default height                                                             
  return MENU_CELL_BASIC_HEADER_HEIGHT;
}

void menu_select_callback(MenuLayer *menu_layer, MenuIndex *cell_index, 
			  void *data) {
  switch (cell_index->row) {
  case 0:
    aqueues_show(); // the admin_queues.c should initialize the queues a user owns when we call aqueues_init() in queuebble.c
    break;
  case 1:
    mqueues_show();
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


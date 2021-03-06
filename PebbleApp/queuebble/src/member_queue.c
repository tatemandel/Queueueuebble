#include <pebble.h>
#include "home.h"
#include "member_queue.h"
#include "member.h"
#include "mini-printf.h"

// should eventually be parametrized by the num of members in the queue
#define NUM_MENU_ITEMS 1
#define NUM_MENU_SECTIONS 1

static Window *window;
static MenuLayer *menu_layer;
static TextLayer *text_layer;

// For functions below eventually cell_index-> row should index 
// into an an array of members and this would be dependent on the
// queue at that index

mmember mmem[20];
int msize = 0;
int mid = 0;

Layer *getMQueueWindowLayer() {
  Layer *window_layer = window_get_root_layer(window);
  return window_layer;
}

static void menu_draw_row_callback(GContext* ctx, const Layer *cell_layer, 
				   MenuIndex *cell_index, void *data) {
  int i = cell_index->row;
  if (i < 0) return;
  mmember a = mmem[i];
  char sub[20];
  mini_snprintf(sub, 19, "Position: %d", a.pos);
  menu_cell_basic_draw(ctx, cell_layer, a.username, sub, NULL);
}

static uint16_t menu_get_num_rows_callback(MenuLayer *menu_layer, 
					   uint16_t section_index, void *data) {
  switch (section_index) {
  case 0:
    return msize;
  default:
    return 0;
  }
}

// Here we draw what each header is                                    
static void menu_draw_header_callback(GContext* ctx, const Layer *cell_layer, uint16_t section_index, void *data) {
  // Determine which section we're working with 
  switch (section_index) {
  case 0:
    // Draw title text in the section header, should eventually say
    // "Member of 'Queue Name'"
    menu_cell_basic_header_draw(ctx, cell_layer, "Members of This Queue");
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

static void menu_select_callback(MenuLayer *menu_layer, MenuIndex *cell_index, 
			  void *data) {
  int i = cell_index->row;
  if (i < 0) return;
  char *username = get_username();
  if (strcmp(username, mmem[i].username) == 0) {
    member_show(mmem[i]);
  }
}

static void window_load(Window *window) {
  Layer *window_layer = window_get_root_layer(window);
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

  text_layer = text_layer_create(bounds);
  text_layer_set_text(text_layer, "There are no members in your queue. Encourage users to join your queue.");

  if (msize > 0) {
    menu_layer_set_click_config_onto_window(menu_layer, window);
    layer_add_child(window_layer, menu_layer_get_layer(menu_layer));
  }
  else {
    window_set_click_config_provider(window, NULL);
    layer_add_child(window_layer, text_layer_get_layer(text_layer));
  }
}

static void window_unload(Window *window) {
  menu_layer_destroy(menu_layer);
}

static void window_appear(Window *window) {
  Layer *window_layer = window_get_root_layer(window);
  layer_remove_child_layers(window_layer);
  if (msize > 0) {
    menu_layer_set_click_config_onto_window(menu_layer, window);
    layer_add_child(window_layer, menu_layer_get_layer(menu_layer));
  }
  else {
    window_set_click_config_provider(window, NULL);
    layer_add_child(window_layer, text_layer_get_layer(text_layer));
  }
}

void mqueue_init(void) {
  window = window_create();
  window_set_window_handlers(window, (WindowHandlers) {
    .load = window_load,
    .unload = window_unload,
    .appear = window_appear,
  });
}

void mqueue_deinit(void) {
  window_destroy(window);
}

void mqueue_show(int id) {
  mid = id;
  const bool animated = true;
  window_stack_push(window, animated);
}

void mqueue_add(char *username, int id, int pos, int status) {
  mmember m;
  strcpy(m.username, username);
  m.id = id;
  m.pos = pos;
  m.status = status;
  mmem[pos] = m;
  if (pos + 1 > msize) msize = pos + 1;
}

void mqueue_reset() {
  msize = 0;
}

int get_mid() {
  return mid;
}

void set_mid(int id) {
  mid = id;
}

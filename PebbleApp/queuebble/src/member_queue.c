#include <pebble.h>
#include "member_queue.h"
#include "member.h"
#include "mini-printf.h"

// should eventually be parametrized by the num of members in the queue
#define NUM_MENU_ITEMS 1
#define NUM_MENU_SECTIONS 1

static Window *window;
static MenuLayer *menu_layer;

// For functions below eventually cell_index-> row should index 
// into an an array of members and this would be dependent on the
// queue at that index

typedef struct mmember {
  char username[20];
  int id;
  int pos;
} mmember;

mmember mmem[20];
int msize = 0;

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
  switch (cell_index->row) {
  case 0:
    member_show();
    break;
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

  menu_layer_set_click_config_onto_window(menu_layer, window);

  layer_add_child(window_layer, menu_layer_get_layer(menu_layer));
}

static void window_unload(Window *window) {
  menu_layer_destroy(menu_layer);
}

void mqueue_init(void) {
  window = window_create();
  window_set_window_handlers(window, (WindowHandlers) {
    .load = window_load,
    .unload = window_unload,
  });
}

void mqueue_deinit(void) {
  window_destroy(window);
}

void mqueue_show(void) {
  const bool animated = true;
  window_stack_push(window, animated);
}

void mqueue_add(char *username, int id, int pos) {
  mmember m;
  strcpy(m.username, username);
  m.id = id;
  m.pos = pos;
  mmem[pos] = m;
  if (pos + 1 > msize) msize = pos + 1;
}

void mqueue_reset() {
  msize = 0;
}

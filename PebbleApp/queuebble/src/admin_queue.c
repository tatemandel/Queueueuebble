#include <pebble.h>
#include "admin_queue.h"
#include "admin.h"
#include "mini-printf.h"

#define NUM_MENU_ITEMS 1
#define NUM_MENU_SECTIONS 1

// Also need some struct for members

static Window *window;
static MenuLayer *menu_layer;
static TextLayer *text_layer;

amember mem[20];
int asize = 0;

// For functions below eventually cell_index-> row should index 
// into an an array of members and this would be dependent on the
// queue at that index

static void menu_draw_row_callback(GContext* ctx, const Layer *cell_layer, 
				   MenuIndex *cell_index, void *data) {
  int i = cell_index->row;
  if (i < 0) return;
  amember a = mem[i];
  char sub[20];
  mini_snprintf(sub, 19, "Position: %d", a.pos);
  menu_cell_basic_draw(ctx, cell_layer, a.username, sub, NULL);
}

// Here we draw what each header is                                    
static void menu_draw_header_callback(GContext* ctx, const Layer *cell_layer, uint16_t section_index, void *data) {
  // Determine which section we're working with 
  switch (section_index) {
  case 0:
    // Draw title text in the section header, should eventually say
    // "Member of 'Queue Name'"
    menu_cell_basic_header_draw(ctx, cell_layer, "Members of Your Queue");
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

static uint16_t menu_get_num_rows_callback(MenuLayer *menu_layer, 
					   uint16_t section_index, void *data) {
  switch (section_index) {
  case 0:
    return asize;
  default:
    return 0;
  }
}

static void menu_select_callback(MenuLayer *menu_layer, MenuIndex *cell_index, void *data) {
  int i = cell_index->row;
  if (i < 0) return;
  admin_show(mem[i]);
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

  if (asize > 0) {
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
  if (asize > 0) {
    menu_layer_set_click_config_onto_window(menu_layer, window);
    layer_add_child(window_layer, menu_layer_get_layer(menu_layer));
  }
  else {
    window_set_click_config_provider(window, NULL);
    layer_add_child(window_layer, text_layer_get_layer(text_layer));
  }
}

void aqueue_init(void) {
  window = window_create();
  window_set_window_handlers(window, (WindowHandlers) {
    .load = window_load,
    .unload = window_unload,
    .appear = window_appear,
  });
}

void aqueue_deinit(void) {
  window_destroy(window);
}

void aqueue_show(void) {
  const bool animated = true;
  window_stack_push(window, animated);
}

void aqueue_add(char *username, int id, int pos, int status) {
  amember m;
  strcpy(m.username, username);
  m.id = id;
  m.pos = pos;
  m.status = status;
  mem[pos] = m;
  if (pos + 1 > asize) asize = pos + 1;
}

void aqueue_reset() {
  asize = 0;
}

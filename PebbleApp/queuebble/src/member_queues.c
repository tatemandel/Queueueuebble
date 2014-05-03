#include <pebble.h>
#include "member_queues.h"
#include "member_queue.h"

// should eventually be parametrized by the num of queues
// visible to the user
#define NUM_MENU_ITEMS 1

// Also need some struct for queues


static Window *window;
static MenuLayer *menu_layer;

// For functions below eventually cell_index-> row should index 
// into an an array of queues and this would be dependent on the
// queue at that index

static void menu_draw_row_callback(GContext* ctx, const Layer *cell_layer, 
				   MenuIndex *cell_index, void *data) {
  switch (cell_index->row) {
  case 0:
    menu_cell_basic_draw(ctx, cell_layer, "Queue 0", NULL, NULL);
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

static void menu_select_callback(MenuLayer *menu_layer, MenuIndex *cell_index, 
			  void *data) {
  switch (cell_index->row) {
  case 0:
    mqueue_show(); // right now only a stub but we should have this take in a queue struct
    break;
  }
}

static void window_load(Window *window) {
  Layer *window_layer = window_get_root_layer(window);
  GRect bounds = layer_get_frame(window_layer);

  menu_layer = menu_layer_create(bounds);

  menu_layer_set_callbacks(menu_layer, NULL, (MenuLayerCallbacks) {
    .get_num_rows = menu_get_num_rows_callback,
    .draw_row = menu_draw_row_callback,
    .select_click = menu_select_callback, 
  });

  menu_layer_set_click_config_onto_window(menu_layer, window);

  layer_add_child(window_layer, menu_layer_get_layer(menu_layer));
}

static void window_unload(Window *window) {
  menu_layer_destroy(menu_layer);
}

void mqueues_init(void) {
  window = window_create();
  window_set_window_handlers(window, (WindowHandlers) {
    .load = window_load,
    .unload = window_unload,
  });
}

void mqueues_deinit(void) {
  window_destroy(window);
}

void mqueues_show(void) {
  const bool animated = true;
  window_stack_push(window, animated);
}

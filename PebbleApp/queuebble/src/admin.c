#include <pebble.h>
#include "home.h"
#include "admin.h"

#define NUM_MENU_ITEMS 5
#define NUM_MENU_SECTIONS 1

// should have member passed in from admin_queue.c

static Window *window;
static MenuLayer *menu_layer;

amember curr_amem;

static void menu_draw_row_callback(GContext* ctx, const Layer *cell_layer, 
				   MenuIndex *cell_index, void *data) {
  switch (cell_index->row) {
  case 0:
    menu_cell_basic_draw(ctx, cell_layer, "Not Started", NULL, NULL);
    break;
  case 1:
    menu_cell_basic_draw(ctx, cell_layer, "In Progress", NULL, NULL);
    break;
  case 2:
    menu_cell_basic_draw(ctx, cell_layer, "Remove", NULL, NULL);
    break;
  case 3:
    menu_cell_basic_draw(ctx, cell_layer, "Move Up", NULL, NULL);
    break;
  case 4:
    menu_cell_basic_draw(ctx, cell_layer, "Move Down", NULL, NULL);
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
    menu_cell_basic_header_draw(ctx, cell_layer, "Admin Options");
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
    // change status to not started
    update_status(curr_amem.username, curr_amem.id, 0);
    break;
  case 1:
    // change status to in progress
    update_status(curr_amem.username, curr_amem.id, 1);
    break;
  case 2:
    // remove from queue
    update_status(curr_amem.username, curr_amem.id, 2);
    break;
  case 3:
    // move up
    update_status(curr_amem.username, curr_amem.id, 3);
    break;
  case 4:
    // move down
    update_status(curr_amem.username, curr_amem.id, 4);
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

void admin_init(void) {
  window = window_create();
  window_set_window_handlers(window, (WindowHandlers) {
    .load = window_load,
    .unload = window_unload,
  });
}

void admin_deinit(void) {
  window_destroy(window);
}

void admin_show(amember a) {
  curr_amem = a;
  const bool animated = true;
  window_stack_push(window, animated);
}

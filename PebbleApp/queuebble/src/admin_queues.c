#include <pebble.h>
#include "home.h"
#include "admin_queues.h"
#include "admin_queue.h"
#include "mini-printf.h"

// should eventually be parametrized by the num of queues
// visible to the user
#define NUM_MENU_SECTIONS 1

typedef struct aqueue {
  char name[32];
  int id;
  int size;
  int status;
} aqueue;

// Also need some struct for queues

static Window *window;
static MenuLayer *menu_layer;
static TextLayer *text_layer;

aqueue aqueues[20];
int aindex = 0;

// For functions below eventually cell_index-> row should index 
// into an an array of queues and this would be dependent on the
// queue at that index
Layer *getAdminWindowLayer() {
  Layer *window_layer = window_get_root_layer(window);
  return window_layer;
}

static void menu_draw_row_callback(GContext* ctx, const Layer *cell_layer, 
				   MenuIndex *cell_index, void *data) {
  int i = cell_index->row;
  if (i < 0) return;
  char sub[20];
  mini_snprintf(sub, 19, "Size: %d <%s>", aqueues[i].size, aqueues[i].status ? "CLOSED" : "OPEN");
  menu_cell_basic_draw(ctx, cell_layer, aqueues[i].name, sub, NULL);
}

// Here we draw what each header is                                    
static void menu_draw_header_callback(GContext* ctx, const Layer *cell_layer, uint16_t section_index, void *data) {
  // Determine which section we're working with 
  switch (section_index) {
  case 0:
    // Draw title text in the section header                          
    menu_cell_basic_header_draw(ctx, cell_layer, "Queues I Own");
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
    return aindex;
  default:
    return 0;
  }
}

static void menu_select_callback(MenuLayer *menu_layer, MenuIndex *cell_index, 
			  void *data) {
  int i = cell_index->row;
  if (i > aindex) return;
  aqueue q = aqueues[i];
  //layer_remove_from_parent(menu_layer_get_layer(menu_layer));
  aqueue_reset();
  load_queue(q.id, "aqueue");
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

  text_layer = text_layer_create(bounds);
  text_layer_set_text(text_layer, "You have no Queues add. Go to our webapp to add some.");

  if (aindex > 0) {
    layer_add_child(window_layer, menu_layer_get_layer(menu_layer));
  }
  else {
    layer_add_child(window_layer, text_layer_get_layer(text_layer));
  }
}

static void window_unload(Window *window) {
  menu_layer_destroy(menu_layer);
}

static void window_appear(Window *window) {
  Layer *window_layer = window_get_root_layer(window);
  layer_remove_child_layers(window_layer);
  if (aindex > 0) {
    layer_add_child(window_layer, menu_layer_get_layer(menu_layer));
  }
  else {
    layer_add_child(window_layer, text_layer_get_layer(text_layer));
  }
}

void aqueues_init(void) {
  window = window_create();
  window_set_window_handlers(window, (WindowHandlers) {
    .load = window_load,
    .unload = window_unload,
    .appear = window_appear,
  });
}

void aqueues_deinit(void) {
  window_destroy(window);
}

void aqueues_show(void) {
  const bool animated = true;
  window_stack_push(window, animated);
}

void aqueues_add(int size, int id, char* name, int status) {
  aqueue q;
  strcpy(q.name, name);
  q.size = size;
  q.id = id;
  q.status = status;
  aqueues[aindex++] = q;
}

void aqueues_reset() {
  aindex = 0;
}

void aqueues_clean(int id, int num) {
  int i = 0;
  for (i = 0; i < 20; i++) {
    if (aqueues[i].id == id) {
      aqueues[i].size = num;
      break;
    }
  }
}

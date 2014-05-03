#include <pebble.h>
#include "admin.h"
#include "home.h"
#include "member.h"
#include "admin_queue.h"
#include "admin_queues.h"
#include "member_queue.h"
#include "member_queues.h"

static void init(void) {
  home_init();
  aqueues_init();
  aqueue_init();
  admin_init();
  mqueues_init();
  mqueue_init();
  member_init();
}

static void deinit(void) {
  home_deinit();
  aqueues_deinit();
  aqueue_deinit();
  admin_deinit();
  mqueues_deinit();
  mqueue_deinit();
  member_deinit();
}

int main(void) {
  init();
  app_event_loop();
  deinit();

  return 0;
}

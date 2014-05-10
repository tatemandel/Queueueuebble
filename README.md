=====
Queuebble
=====

###User Manual###

**Home Screen**
![home](https://raw.github.com/tatemandel/Queueueuebble/master/images/home.png)
The home screen allows one to register or login. There are buttons in the top left of for these actions. If already logged in, one can click on the dashboard button in the top right to navigate to the user’s dashboard. 

**Login**
![login](https://raw.github.com/tatemandel/Queueueuebble/master/images/login.png)
The login screen allows one to login to the web app. It requires the username and password.  On the bottom right of the button there is a link for password reset and a link back to the home page.  The password reset link allows one to enter his or her email, which will then send directions via email to the user to reset his or her password.

**Dashboard**
![dash](https://raw.github.com/tatemandel/Queueueuebble/master/images/dashboard.png)
On the dashboard, one can both create a queue and search for other queues owned by any user. On the left side, there is an input box to create a queue. A user should type a valid string into the field and press “Create” to create a new queue. This will cause the user to create a new queue object that will be displayed under “Queues Owned” on the dashboard. These queues will be those owned by you, including those that you have created. For each queue on this list, there is an option to close that queue. This means that the queue will not allow anyone to add him or herself to it until it is opened again, but as an owner you may still manage it normally. The queues each also have a small “x” button to the right of them in the list. This button will delete the queue. The middle row contains the name of each queue in which you are a member. The list contains links to each queue that you may click to navigate to that queue’s page. The right list is the list of queues that you have marked as a favorite. These queues can be removed from the list by navigating to the queue and pressing the appropriate button described in the Queue Screen section. The final part of the dashboard is a search option. One may enter a search term into the textbox on the left menu and press “Search” to see results matching the query.

**Search Results**
![search](https://raw.github.com/tatemandel/Queueueuebble/master/images/search.png)
After searching from the dashboard, the user is redirected to the page with search results. This page separates results into two sections. The first is the list of queues and their links that contain the search terms. The second list is a list of users that contain the search term. These are all links to the users or queues.

**Queues**
![queue](https://raw.github.com/tatemandel/Queueueuebble/master/images/queue.png)
This screen contains the data associated with a single queue. This page can be viewed by an owner and a non-owner, and it has different options for each.  In either case, there is a list of users in boxes on the left margin. This is the queue itself. The top of the queue means the first to be handled, and the bottom is the most recent addition to the queue.



###Pebble App###
**Home Screen:**
The home screen has two options. The first is “Owner” and takes the user to a page displaying all queues that he or she owns. The second is “Member” and this takes the user to a page displaying a list of all queues he or she is a member of.

**Owned Queue Screen:**
This screen shows all queues owned by a user. Each queue contains the name of the queue, the size of the queue, and whether it is open or closed. When clicking on a queue, the particular queue and all members are displayed.

**Member Queue Screen:**
This screen shows all queues of which the user is a member. Each queue shows the user’s position as well as the name of the queue and its owner. When clicking on a queue, the particular queue and all members are shown.

**Members Screen:**
This page is shown for owned queues and queues that you are a member in. Each element is a member of the queue with name and position displayed. For an owner, each member can be clicked on to display options. For a member, the member can only select him or herself. 

**Owner Options:**
The owner of a queue can change the status of a user to “in progress” or “not started” from the options page. The owner can also remove that user or move him or her up or down in the queue by pressing the associated buttons.

**Member Options:**
The member of a queue can add that queue to his or her favorites and also can remove him or herself from that queue through the buttons on this options menu.



*Run on pebble:*
make
pebble install [ip address]

*Run database:*
python manage.py syncdb
./manage.py migrate

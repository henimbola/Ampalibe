Messenger API 
=============

list of methods for sending messages to messenger

.. note::

   All returns of these functions are a POST Requests <Response>



send_message
____________

This method allows you to send a text message to the given recipient,
Note that the number of characters to send is limited to 2000 characters


**Ref**: https://developers.facebook.com/docs/messenger-platform/send-messages#sending_text

**Args**:

    *dest_id (str)*: user id facebook for the destination

    *message (str)*: message want to send

**Example**:

.. code-block:: python

    chat.send_message(sender_id, "Hello world")


send_action
____________

This method is used to simulate an action on messages.
example: view, writing.

Action available: ['mark_seen', 'typing_on', 'typing_off']

**Ref**:  https://developers.facebook.com/docs/messenger-platform/send-messages/sender-actions

**Args**:

    *dest_id (str)*: user id facebook for the destination
    
    *action (str)*: action ['mark_seen', 'typing_on', 'typing_off']

**Example**:

.. code-block:: python

    chat.send_action(sender_id, "mark_seen")


send_quick_reply
_________________

.. image:: https://raw.githubusercontent.com/iTeam-S/Ampalibe/main/docs/source/_static/quickrep.png

Quick replies provide a way to present a set of up to 13 buttons 
in-conversation that contain a title and optional image, and appear
prominently above the composer. 

You can also use quick replies 
to request a person's location, email address, and phone number.


**Ref**:  https://developers.facebook.com/docs/messenger-platform/send-messages/quick-replies

**Args**:

    *dest_id (str)*: user id facebook for the destoination

    *quick_rep(list of Button)*: list of the different quick_reply to send a user
    
    *text (str)*: A text of a little description for each <quick_reply>

**Example**:

.. code-block:: python
    
    from ampalibe.ui import QuickReply
    ... 

    quick_rep = [
        QuickReply(
            title="Angela",
            payload="/membre",
            image_url="https://i.imgflip.com/6b45bi.jpg"
        ),
        QuickReply(
            title="Rivo",
            payload="/membre",
            image_url="https://i.imgflip.com/6b45bi.jpg"
        ),
    ]

    # next=True in parameter for displaying directly next list quick_reply
    chat.send_quick_reply(sender_id, quick_rep, 'who do you choose ?')

.. code-block:: python
    
    from ampalibe.ui import QuickReply
    ... 

    quick_rep = [
        QuickReply(
            title=f"response {i+1}",
            payload= Payload("/response", item=i+1)
            image_url="https://i.imgflip.com/6b45bi.jpg"
        ) 

        for i in range(30)
    ]

    # put a value in `next` parameter to show directly next options with the specified word.
    chat.send_quick_reply(sender_id, quick_rep, 'who do you choose ?', next='See More')


send_template
_____________

.. image:: https://raw.githubusercontent.com/iTeam-S/Ampalibe/main/docs/source/_static/template.png

The method send_template represent a Message templates who offer a way for you 
to offer a richer in-conversation experience than standard text messages by integrating
buttons, images, lists, and more alongside text a single message. Templates can be use for 
many purposes, such as displaying product information, asking the messagerecipient to choose 
from a pre-determined set of options, and showing search results.

For this, messenger only validates 10 templates
for the first display, so we put the parameter
<next> to manage these numbers if it is a number of 
elements more than 10.
So, there is a quick_reply which acts as a "next page"
displaying all requested templates
        

**Ref**: https://developers.facebook.com/docs/messenger-platform/send-messages/template/generic

**Args**:

    *dest_id (str)*: user id facebook for the destination
    
    *elements(list of Element)*: the list of the specific elements to define the structure for the template
    
    *quick_rep(list of QuickReply)*: addition quick reply at the bottom of the template
    
    *next(bool)*: this params activate the next page when elements have a length more than 10

**Example**:

.. code-block:: python

    from ampalibe import Payload
    from ampalibe.ui import Element, Button

    ...

    list_items = []

    for i in range(30):
        buttons = [
            Button(
                type="postback",
                title="Get item",
                payload=Payload("/item", id_item=i+1),
            )
        ]

        list_items.append(
            Element(
                title="iTem",
                image_url="https://i.imgflip.com/6b45bi.jpg",
                buttons=buttons,
            )
        )

    # next=True for displaying directly next page button.
    chat.send_template(sender_id, list_items, next=True)

    # next=<word> for displaying directly next page button with custom text.
    # chat.send_template(sender_id, list_items, next='Next page')

send_file_url
_____________

The Messenger Platform allows you to attach assets to messages, including audio, 
video, images, and files.All this is the role of this Method. The maximum attachment
size is 25 MB.

**Args**:

    *dest_id (str)*: user id facebook for destination

    *url (str)*: the origin url for the file

    *filetype (str, optional)*: type of showing file["video","image","audio","file"]. Defaults to 'file'.


**Ref**:  https://developers.facebook.com/docs/messenger-platform/send-messages#url



**Example**:

.. code-block:: python

    chat.send_file_url(sender_id, 'https://i.imgflip.com/6b45bi.jpg', filetype='image')



send_file
____________

This method send an attachment from file

**Ref**:  https://developers.facebook.com/docs/messenger-platform/send-messages#file

**Args**:

    *dest_id (str)*: user id facebook for the destination
    
    *file (str)*: name of the file in local folder 
    
    *filetype (str, optional)*: type of the file["video","image",...]. Defaults to "file".
    
    *filename (str, optional)*: A filename received for de destination . Defaults to name of file in local.


**Example**:

.. code-block:: python

    chat.send_file(sender_id, "mydocument.pdf")

    chat.send_file(sender_id, "intro.mp4", filetype='video')

    chat.send_file(sender_id, "myvoice.m4a", filetype='audio')


send_media
____________

Method that sends files media as image and video via facebook link.
This model does not allow any external URLs, only those on Facebook.


**Ref**:  https://developers.facebook.com/docs/messenger-platform/send-messages/template/media

**Args**:

    *dest_id (str)*: user id facebook for the destination
    
    *fb_url (str)*: url of the media to send on facebook

    *media_type (str)*: the type of the media who to want send, available["image","video"]

**Example**:

.. code-block:: python

    chat.send_media(sender_id, "https://www.facebook.com/iTeam.Community/videos/476926027465187", 'video')


send_button
____________

.. image:: https://raw.githubusercontent.com/iTeam-S/Ampalibe/main/docs/source/_static/button.png

The button template sends a text message with 
up to three buttons attached. This template gives 
the message recipient different options to choose from, 
such as predefined answers to questions or actions to take.

**Ref**:  https://developers.facebook.com/docs/messenger-platform/send-messages/template/button

**Args**:

    *dest_id (str)*: user id facebook for the destination
    
    *buttons(list of Button)*: The list of buttons who want send

    *text (str)*: A text to describe the fonctionnality of the buttons

**Example**:

.. code-block:: python

    from ampalibe.ui import Button

    buttons = [
        Button(
            type='postback',
            title='Informations',
            payload='/contact'
        )
    ]

    chat.send_button(sender_id, buttons, "What do you want to do?")


get_started
____________

Method that GET STARTED button
when the user talk first to the bot.


**Ref**:  https://developers.facebook.com/docs/messenger-platform/reference/messenger-profile-api/get-started-button

**Args**:

    *dest_id (str)*: user id facebook for the destination
    
    *payload (str)*: payload of get started, default: '/'


**Example**:

.. code-block:: python

    chat.get_started()


persistent_menu
________________

The Persistent Menu disabling the composer best practices allows you to have an always-on 
user interface element inside Messenger conversations. This is an easy way to help people 
discover and access the core functionality of your Messenger bot at any point in the conversation

**Ref**:  https://developers.facebook.com/docs/messenger-platform/send-messages/persistent-menu

**Args**:

    *dest_id (str)*: user id for destination

    *persistent_menu (list of dict) | (list of Button)*: the elements of the persistent menu to enable

    *action (str, optional)*: the action for benefit["PUT","DELETE"]. Defaults to 'PUT'.
    
    *locale [optionnel]*

    *composer_input_disabled [optionnel]*

**Example**:

.. code-block:: python

    from ampalibe.ui import Button
    ...

    persistent_menu = [
        Button(type='postback', title='Menu', payload='/payload')
        Button(type='postback', title='Logout', payload='/logout')
    ]

    chat.persistent_menu(sender_id, persistent_menu)


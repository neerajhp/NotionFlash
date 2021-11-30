# NotionFlash

This is an Anki add on in development that will allow automatically convert your Notion study notes into Anki flash cards. The Anki deck created will remain synchronised with your notes, removing the need to rehash them into flash cards.

## Motivation

NotionFlash was created as an integration between the wonderful document management platform Notion and the excellent open-source flash card utility Anki. The goal is to automate the creation of Anki flash cards derived from selected pages in a Notion workspace.

## Installation

You can run this project just like any python script but at this stage in development it does require quite abit of initial setup.

### Environment

To run this script requires abit of setup. Download the folder AnkiBots and within it create a .env file with the following variables

```
NOTION_SECRET=...
DECK=...
PAGE_ONE=...
PAGE_TWO=...
PAGE_THREE=...
```

The value for NOTION_SECRET is your Notion authentication token. You can find information about this here [Notion API Authorisation](https://developers.notion.com/reference/authentication) and how to setup an API endpoint and share your Notion pages to it.

The value for DECK is the name of the ANKI deck you wish to add cards to.

The values for PAGE_ONE, PAGE_TWO, PAGE_THREE, PAGE_XXX and so on are Notion page id's. You can find out about page id's here [Notion API Getting Started](https://developers.notion.com/docs/getting-started). You must format your page id as is in the following example

```
...
PAGE_ONE=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
...
```

You must then update line 26 in the main file with the page names you have specified in the .env as well as a tag for each respective page. For example

```
...
DATABASES = [{"Database":os.getenv("PAGE_ONE"), "cardTag": "PageOneTag"}, {"Database":os.getenv("PAGE_TWO"), "cardTag": "PageTwoTag"}, {"Database":os.getenv("PAGE_THREE"), "cardTag": "PageThreeTag"}]
...
```

### AnkiConnect

You must install the Anki add on [AnkiConnect](https://ankiweb.net/shared/info/2055492159) and have Anki open when you run the script

## How it works

This script leverages the Notion beta API and Notion toggle lists to create simple Question and Answer Anki cards. In order for the script to identify notes that you wish to convert into a card simply create a toggle (/toggle) in your Notion page with the Question as the title and the Answer as the nested content.

The script will run through all the toggle lists on your page and add them to your specified Anki deck. Cards are not duplicated the following formats are supported - numbered lists, bullet points, images.

## Contributing

This project is in its infancy any and all ideas are welcome!

## Licence

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Licensed under the [MIT Licence](https://github.com/medusajs/medusa/blob/master/LICENSE)

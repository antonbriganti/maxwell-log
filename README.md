# maxwell-log 
an in-character journal/blog. less of a code thing, more of a creative writing thing. 

## what's the deal here?
### who's Maxwell? 
Maxwell's a character I'm playing in the [Lancer TTRPG](https://massif-press.itch.io) campaign I'm part of.

### what is this? 
I've decided to maintain a basic journal for Maxwell to cover his musings and thoughts on the campaign as we play it. It's a fun way to roleplay and I also just don't really do any creative writing so it's a good excuse to stretch those muscles a bit. 

## tech stack 
### website
this is built to be as lightweight as possible, so I've just stuck to markdown for the writing and HTML+CSS for rendering.

I've used the following things:
- [pico css](https://picocss.com) for style base etc.
- [marked](https://marked.js.org) for rendering markdown 

### templating 
I built the world's worst templating engine for this. I didn't feel like using anything big like Jekyll or Astro as part of this so I wrote a basic script (mostly stolen from my blog repo) to do some file creation and templating.

the basic flow is:
0. create new html and markdown files from `_templates` directory 
1. use `sed` to insert a title and markdown file name into the html 
2. use a terrible mix of `sed` + `printf` to insert a reference to the new entry into `index.html` (thank you ChatGPT, this sucks but it works and I was too lazy to find a better solution at 3am)

### deploy 
currently hosted on my home server and shared with friends

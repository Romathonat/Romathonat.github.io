

To convert notebooks to markdown:

``` bash
jupyter-nbconvert --to markdown analyse_coronavirus.ipynb 
```

To convert a markdown from notion to a ready to post markdown, extract images folder + mardown file to script/, then:

``` bash
sudo python3 notion_to_post.py 
```
and enter the name of the markdown file. It will extract images to the right place, as well as transform the markdown correctly to have a nice post.


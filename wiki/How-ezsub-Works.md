# How ezsub works

## It is all about laziness

So many volunteered translators make subtitles and upload them on websites like [subscene](https://subscene.com).  
But downloading subtitles for each episode of a TV series or many versions of a movie is a long procedure. You have to:

``` pseudocode
do {

    visit main page of the site
    search a title
    select a match
    go to the selected page
    look over maybe 100 or 1000 subtitles on this page, even they are not in your desired language
    choose which subtitless match your language, episode, encoder, uploader
    open them in new tabs
    click the download buttons and save them
    extract them
    move extracted subtitles to the folder next to your media file

} while ("subtitle is not crap" and "subtitle is sync with your media")
```

Sometimes you have to check if there is a subtitle for new episode that aired recently. You must do this procedure multiple times without even getting a subtitle because it is not available yet.

Trust me! I done it hundreds of times and it is exhausting, boring and annoying but mandatory to enjoy watching your favorite movies and TV series.  

`ezsub` is basically automated simulation of this procedure and

- takes a title
- searches the title through a given mirror of subscene
- auto-selects best match (not 100% accurate) or asks you to select
- filters out subtitles based on languages you ordered
- filters out previously downloaded subtitles which stored in a cache folder
- downloads new subtitles and stores them in the cache folder
- extracts them to a destination you ordered and labels extracted subtitles with language they have
- deletes duplicated subtitles (with exactly same content regardless of their names)
- opens the destination folder after it is done

Considering size of subtitles that are very small, `ezsub` will download all new subtitles of given languages in every call against a title. For example all Persian and English subtitles uploaded for seventh season of game of thrones is about only 24.79 MB (559 zip files)

Because `ezsub` caches downloaded subtitles, you can extract them again with `ezsub` itself. It has a sub-command to do this. Procedure to extract from cache is something like download process.

`ezsub` creates a config file and sets some default behavior and options to use less arguments in each call. Options such as which mirror, language you prefer and your default destination. Behavior such as if you want to open destination folder after it is done.

[Back to Home](./ReadMe.md)

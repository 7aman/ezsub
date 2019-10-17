# Login

```shell
ezsub login
```

Since June 2019, subscene added google re-captcha. If user logs in, this captcha is not required.  
At now (June 2019) it is not required to pass username and password to this command. It gets a token from login page itself without authentication.  
If `subscene` is returning too much `Bad Request`, maybe it needs to be logged in. Use this command first to get a new token. Then try again.

[Back to Home](./ReadMe.md)

# Login

To get a new token to use for downloading from `subacene`:

```shell
ezsub login

# short version
ezsub l
```

Since June 2019, subscene added google re-captcha. If user logs in, this captcha is not required.  
But until now (June 2020) it is not required to actually have a username and password to this command. `ezsub` gets the required token from login page without authentication.  
If `subscene` is returning too much `Bad Request`, run this command to get a new token. Then try again.

[Back to Home](./ReadMe.md)

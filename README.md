
# MiWIFI 4 Router Api

The project started from the necessity of doing some operation on my WiFi router fast. The version 4 of MiWiFI Router, hasn't an English version and can be used only in Chinese from the web. So, I decided to rewrite the backend for this app, and use it where I want (Telegram Bot, Discord Bot, a custom web app).

## Examples
Using this is very easy. Initialize MiRouter object like this

    from MiRouter import MiRouter
    
    api = MiRouter()
    login_result = api.login(PASSWORD)
And you can use endpoint just accessing the api.name_of_method

If you want to turn your primary WLAN interface ON, you can just:
    
    api.set_wifi_status(wifi_index=1, status=1)


## Endpoints

| Endpoint  | Parameters  | Description  |
|---|---|---|
| get_device_list  |  //  | Get the information about all devices connected  |
| get_wifi_detail  |  //  | Getting all information about WIFI (List and other information)  |
| set_wifi_status  | wifi_index: number, status = 0: number  | Enable or Disable the WIFI interface  |

## TODO
- Adding other endpoints
- Pushing unittest

In my plains there is an Angular web app cause the Mi Router application, which can be found in Apple Store or Play Store, isn't so good. If the network is slow, the app doens't load and it's not efficient.
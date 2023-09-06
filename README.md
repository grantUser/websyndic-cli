# websyndic-cli

websyndic-cli is a Python script designed to automate certain tasks on the [WebSyndic](https://www.websyndic.com) website, a platform for generating website traffic. This script provides functionality to log in to your WebSyndic account and generate points for website traffic.

## Features

- **Login**: Automate the login process to your WebSyndic account.
- **Generate Points**: Automatically generate website traffic points.
- **Light Viewer Mode**: Optional mode to generate points with a light viewer.

## Getting Started

To get started with WebSyndic, follow these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/WebSyndic.git
   ```

2. Install the required dependencies. You can use pip:

   ```bash
   pip install -r requirements.txt
   ```

3. Configure your NordVPN credentials and server location in the nordvpn.get_nordvpn_proxy function within the __main__ block of the websyndic.py file.

4. Run the script:

   ```bash
   python websyndic.py
   ```

   This will execute the script, logging in to your WebSyndic account and generating website traffic points.

## Configuration

In order to use the script, you need to provide your NordVPN credentials and specify the server location you want to use. You can do this in the __main__ block of the websyndic.py file:

```python
  proxies = nordvpn.get_nordvpn_proxy(
      nord_account_user="your-nordvpn-username",
      nord_account_password="your-nordvpn-password",
      nord_account_server="JP",  # Replace with your desired server location
  )
```
Make sure to replace "your-nordvpn-username" and "your-nordvpn-password" with your NordVPN credentials and choose the appropriate server location by replacing "JP".

## Usage
You can use the script by running it as shown in the "Getting Started" section. Additionally, you can modify the websyndic.py script to suit your specific requirements.

```python
# Example usage
websyndic.make_light_points(
    light_viewer="https://www.websyndic.com/wv3/FR/?qs=XXXXXXXX"
)
```

## Disclaimer
Please use this script responsibly and in accordance with the terms of service of the WebSyndic website. Automated scripts like this should be used for legitimate purposes only.

## License
This project is licensed under the MIT License - see the __LICENSE__ file for details.
